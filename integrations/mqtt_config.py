"""Puntos de integracion entre la aplicacion y procesos externos como cola SQL o MQTT.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from services.jobtrack.jobtrack_config_service import JobtrackConfigService


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "mqtt.json"
EXAMPLE_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "docs" / "configuracion" / "mqtt.example.json"
)
AUTO_STATION_ID = "auto"


# Bloque CDLform: clase MqttConfig; agrupa estado y comportamiento de esta parte del flujo.
@dataclass(frozen=True)
class MqttConfig:
    broker_host: str
    broker_port: int
    username: str
    password: str
    station_id: str
    topic_prefix: str

    # Bloque CDLform: funcion/metodo station_topic; encapsula una operacion del flujo del modulo.
    @property
    def station_topic(self) -> str:
        if not self.station_id or self.station_id.lower() == AUTO_STATION_ID:
            raise ValueError(
                "station_id esta en auto. Resuelva la estacion local o use topic_for_station()."
            )
        return self.topic_for_station(self.station_id)

    # Bloque CDLform: funcion/metodo topic_for_station; encapsula una operacion del flujo del modulo.
    def topic_for_station(self, station_id: str) -> str:
        prefix = self.topic_prefix.strip().strip("/")
        station = str(station_id or "").strip().strip("/")
        if not station:
            raise ValueError("La estacion destino no puede venir vacia.")
        return f"{prefix}/{station}/eventos"


# Bloque CDLform: funcion/metodo load_mqtt_config; encapsula una operacion del flujo del modulo.
def load_mqtt_config(
    config_path: str | Path | None = None,
    *,
    resolve_station: bool = True,
) -> MqttConfig:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Copia {EXAMPLE_CONFIG_PATH} como mqtt.json y ajusta los datos."
        )

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    station_id = str(data.get("station_id") or AUTO_STATION_ID).strip()
    if resolve_station and (not station_id or station_id.lower() == AUTO_STATION_ID):
        # En estaciones, "auto" reutiliza el mismo origen que el modo operario.
        station_id = JobtrackConfigService().obtener_estacion_local()

    return MqttConfig(
        broker_host=str(data.get("broker_host") or "127.0.0.1").strip(),
        broker_port=int(data.get("broker_port") or 1883),
        username=str(data.get("username") or "").strip(),
        password=str(data.get("password") or ""),
        station_id=station_id,
        topic_prefix=str(data.get("topic_prefix") or "cdlform/estaciones").strip(),
    )
