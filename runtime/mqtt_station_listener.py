"""Listener MQTT de estacion. Escucha avisos y dispara main.py --modo auto cuando corresponde.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from integrations.mqtt_config import load_mqtt_config

LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "mqtt_station_listener.log"


# Bloque CDLform: funcion/metodo parse_args; encapsula una operacion del flujo del modulo.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Listener MQTT piloto para CDLform.")
    parser.add_argument("--config", default=None, help="Ruta a config/mqtt.json")
    parser.add_argument(
        "--run-auto",
        action="store_true",
        help="Ejecuta main.py --modo auto cuando llega un mensaje.",
    )
    parser.add_argument(
        "--initial-check",
        action="store_true",
        help="Ejecuta main.py --modo auto una vez al iniciar.",
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
            logging.StreamHandler(sys.stdout),
        ],
    )


# Bloque CDLform: funcion/metodo run_operario_auto; encapsula una operacion del flujo del modulo.
def run_operario_auto(reason: str) -> None:
    command = [sys.executable, str(ROOT_DIR / "main.py"), "--modo", "auto"]
    logging.info("Ejecutando main.py --modo auto. Motivo: %s", reason)
    # El listener sigue vivo mientras la app abre o mantiene una UI activa.
    subprocess.Popen(command, cwd=ROOT_DIR)


# Bloque CDLform: funcion/metodo main; encapsula una operacion del flujo del modulo.
def main() -> int:
    args = parse_args()
    setup_logging()
    config = load_mqtt_config(args.config)

    try:
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise SystemExit(
            "Falta instalar paho-mqtt. Ejecuta: pip install -r requirements.txt"
        ) from exc

    if args.initial_check:
        # Recupera pendientes que aparecieron mientras la estacion estaba apagada.
        run_operario_auto("revision inicial del listener")

    # Bloque CDLform: funcion/metodo on_connect; encapsula una operacion del flujo del modulo.
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            logging.info("Conectado a MQTT %s:%s", config.broker_host, config.broker_port)
            client.subscribe(config.station_topic, qos=1)
            logging.info("Suscrito a %s", config.station_topic)
            return

        logging.error("Conexion MQTT rechazada: %s", reason_code)

    # Bloque CDLform: funcion/metodo on_disconnect; encapsula una operacion del flujo del modulo.
    def on_disconnect(client, userdata, flags, reason_code, properties=None):
        logging.warning("Desconectado de MQTT: %s", reason_code)

    # Bloque CDLform: funcion/metodo on_message; encapsula una operacion del flujo del modulo.
    def on_message(client, userdata, message):
        payload_text = message.payload.decode("utf-8", errors="replace")
        logging.info("Mensaje recibido en %s: %s", message.topic, payload_text)

        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError:
            payload = {"payload": payload_text}

        if args.run_auto:
            run_operario_auto(f"mensaje MQTT {payload.get('id_evento', 'sin id')}")
        else:
            logging.info("Piloto sin --run-auto: no se ejecuto la app.")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if config.username:
        client.username_pw_set(config.username, config.password)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=2, max_delay=30)

    while True:
        try:
            logging.info("Conectando a MQTT %s:%s", config.broker_host, config.broker_port)
            client.connect(config.broker_host, config.broker_port, keepalive=30)
            client.loop_forever(retry_first_connection=True)
        except KeyboardInterrupt:
            logging.info("Listener detenido por usuario.")
            return 0
        except Exception:
            logging.exception("Error en listener MQTT. Reintentando en 5 segundos.")
            time.sleep(5)


# Bloque CDLform: punto de ejecucion directa del modulo desde consola.
if __name__ == "__main__":
    raise SystemExit(main())
