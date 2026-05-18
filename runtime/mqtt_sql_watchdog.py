"""Watchdog central SQL -> MQTT. Vigila eventos pendientes y publica avisos por estacion.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from integrations.mqtt_config import load_mqtt_config
from services.jobtrack.apontamento_query_service import ApontamentoQueryService

DEFAULT_WATCHDOG_CONFIG_PATH = ROOT_DIR / "config" / "mqtt_watchdog.json"
EXAMPLE_WATCHDOG_CONFIG_PATH = (
    ROOT_DIR / "docs" / "configuracion" / "mqtt_watchdog.example.json"
)
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "mqtt_sql_watchdog.log"


# Bloque CDLform: clase WatchdogConfig; agrupa estado y comportamiento de esta parte del flujo.
@dataclass(frozen=True)
class WatchdogConfig:
    poll_interval_seconds: int
    notify_cooldown_seconds: int
    limit: int


# Bloque CDLform: funcion/metodo parse_args; encapsula una operacion del flujo del modulo.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watchdog SQL -> MQTT para eventos_op_pendientes."
    )
    parser.add_argument("--mqtt-config", default=None, help="Ruta a config/mqtt.json")
    parser.add_argument(
        "--watchdog-config",
        default=None,
        help="Ruta a config/mqtt_watchdog.json",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Ejecuta un solo ciclo y termina.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No publica MQTT; solo registra lo que haria.",
    )
    return parser.parse_args()


# Bloque CDLform: funcion/metodo setup_logging; encapsula una operacion del flujo del modulo.
def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


# Bloque CDLform: funcion/metodo load_watchdog_config; encapsula una operacion del flujo del modulo.
def load_watchdog_config(config_path: str | Path | None = None) -> WatchdogConfig:
    path = Path(config_path) if config_path else DEFAULT_WATCHDOG_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Copia {EXAMPLE_WATCHDOG_CONFIG_PATH} como mqtt_watchdog.json."
        )

    data = json.loads(path.read_text(encoding="utf-8"))
    return WatchdogConfig(
        poll_interval_seconds=max(1, int(data.get("poll_interval_seconds") or 10)),
        notify_cooldown_seconds=max(
            1,
            int(data.get("notify_cooldown_seconds") or 300),
        ),
        limit=max(1, int(data.get("limit") or 100)),
    )


# Bloque CDLform: funcion/metodo _normalizar_texto; encapsula una operacion del flujo del modulo.
def _normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


# Bloque CDLform: clase MqttSqlWatchdog; agrupa estado y comportamiento de esta parte del flujo.
class MqttSqlWatchdog:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(
        self,
        *,
        mqtt_config_path: str | Path | None = None,
        watchdog_config_path: str | Path | None = None,
        dry_run: bool = False,
    ) -> None:
        self.mqtt_config = load_mqtt_config(
            mqtt_config_path,
            resolve_station=False,
        )
        self.watchdog_config = load_watchdog_config(watchdog_config_path)
        self.query_service = ApontamentoQueryService()
        self.dry_run = dry_run
        self.notificados: dict[str, datetime] = {}
        self.mqtt_client = None

    # Bloque CDLform: funcion/metodo _obtener_mqtt_client; encapsula una operacion del flujo del modulo.
    def _obtener_mqtt_client(self):
        if self.mqtt_client is not None:
            return self.mqtt_client

        # Mantiene una conexion MQTT viva para no reconectar en cada ciclo SQL.
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError(
                "Falta instalar paho-mqtt. Ejecuta: pip install -r requirements.txt"
            ) from exc

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if self.mqtt_config.username:
            client.username_pw_set(
                self.mqtt_config.username,
                self.mqtt_config.password,
            )
        client.connect(
            self.mqtt_config.broker_host,
            self.mqtt_config.broker_port,
            keepalive=30,
        )
        client.loop_start()
        self.mqtt_client = client
        return client

    # Bloque CDLform: funcion/metodo cerrar; encapsula una operacion del flujo del modulo.
    def cerrar(self) -> None:
        if self.mqtt_client is None:
            return
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        self.mqtt_client = None

    # Bloque CDLform: funcion/metodo _puede_notificar; encapsula una operacion del flujo del modulo.
    def _puede_notificar(self, id_evento: str, ahora: datetime) -> bool:
        ultima_notificacion = self.notificados.get(id_evento)
        if ultima_notificacion is None:
            return True

        # Evita repetir el mismo aviso en cada poll mientras siga pendiente.
        cooldown = timedelta(seconds=self.watchdog_config.notify_cooldown_seconds)
        return ahora - ultima_notificacion >= cooldown

    # Bloque CDLform: funcion/metodo _limpiar_notificados; encapsula una operacion del flujo del modulo.
    def _limpiar_notificados(self, ids_pendientes: set[str]) -> None:
        # Si SQL ya no lista el evento, limpiamos la memoria local del watchdog.
        for id_evento in list(self.notificados):
            if id_evento not in ids_pendientes:
                self.notificados.pop(id_evento, None)

    # Bloque CDLform: funcion/metodo ejecutar_ciclo; encapsula una operacion del flujo del modulo.
    def ejecutar_ciclo(self) -> dict[str, int]:
        eventos = self.query_service.listar_eventos_op_pendientes(
            limit=self.watchdog_config.limit,
            enriquecer_supervisores=False,
        )
        ids_pendientes = {
            _normalizar_texto(evento.get("id_evento"))
            for evento in eventos
            if _normalizar_texto(evento.get("id_evento"))
        }
        self._limpiar_notificados(ids_pendientes)

        cod_recursos = [
            _normalizar_texto(evento.get("cod_recurso"))
            for evento in eventos
            if _normalizar_texto(evento.get("cod_recurso"))
        ]
        # La cola trae CodRecurso; MQTT se enruta por estacion.
        estaciones_por_recurso = (
            self.query_service.listar_estaciones_por_cod_recursos(cod_recursos)
            if cod_recursos
            else {}
        )

        ahora = datetime.now()
        total_publicados = 0
        total_omitidos_cooldown = 0
        total_sin_estacion = 0

        for evento in eventos:
            id_evento = _normalizar_texto(evento.get("id_evento"))
            cod_recurso = _normalizar_texto(evento.get("cod_recurso"))
            estacion = estaciones_por_recurso.get(cod_recurso, "")

            if not id_evento:
                continue

            if not estacion:
                total_sin_estacion += 1
                logging.warning(
                    "Evento %s sin estacion homologada para CodRecurso=%s",
                    id_evento,
                    cod_recurso,
                )
                continue

            if not self._puede_notificar(id_evento, ahora):
                total_omitidos_cooldown += 1
                continue

            topic = self.mqtt_config.topic_for_station(estacion)
            payload = {
                "tipo": "evento_pendiente",
                "id_evento": id_evento,
                "id_apontamento": evento.get("id_apontamento"),
                "estacion": estacion,
                "cod_recurso": cod_recurso,
                "fecha_publicacion": ahora.isoformat(timespec="seconds"),
            }

            if self.dry_run:
                logging.info("DRY RUN publicaria en %s: %s", topic, payload)
            else:
                client = self._obtener_mqtt_client()
                result = client.publish(
                    topic,
                    json.dumps(payload, ensure_ascii=False),
                    qos=1,
                )
                result.wait_for_publish(timeout=10)
                logging.info("Publicado evento %s en %s", id_evento, topic)

            self.notificados[id_evento] = ahora
            total_publicados += 1

        return {
            "consultados": len(eventos),
            "publicados": total_publicados,
            "omitidos_cooldown": total_omitidos_cooldown,
            "sin_estacion": total_sin_estacion,
        }

    # Bloque CDLform: funcion/metodo ejecutar; encapsula una operacion del flujo del modulo.
    def ejecutar(self, *, once: bool = False) -> None:
        logging.info(
            "Iniciando watchdog SQL -> MQTT. broker=%s:%s intervalo=%ss cooldown=%ss limit=%s dry_run=%s",
            self.mqtt_config.broker_host,
            self.mqtt_config.broker_port,
            self.watchdog_config.poll_interval_seconds,
            self.watchdog_config.notify_cooldown_seconds,
            self.watchdog_config.limit,
            self.dry_run,
        )

        while True:
            try:
                resumen = self.ejecutar_ciclo()
                logging.info("Ciclo watchdog: %s", resumen)
            except Exception:
                logging.exception("Error en ciclo watchdog.")

            if once:
                return

            time.sleep(self.watchdog_config.poll_interval_seconds)


# Bloque CDLform: funcion/metodo main; encapsula una operacion del flujo del modulo.
def main() -> int:
    args = parse_args()
    if not os.getenv("CDLFORM_SQL_PROFILE", "").strip():
        os.environ["CDLFORM_SQL_PROFILE"] = "watchdog"

    setup_logging()
    watchdog = MqttSqlWatchdog(
        mqtt_config_path=args.mqtt_config,
        watchdog_config_path=args.watchdog_config,
        dry_run=args.dry_run,
    )
    try:
        watchdog.ejecutar(once=args.once)
    except KeyboardInterrupt:
        logging.info("Watchdog detenido por usuario.")
    finally:
        watchdog.cerrar()
    return 0


# Bloque CDLform: punto de ejecucion directa del modulo desde consola.
if __name__ == "__main__":
    raise SystemExit(main())
