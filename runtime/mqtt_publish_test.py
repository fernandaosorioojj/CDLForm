"""Herramienta de prueba para publicar manualmente mensajes MQTT hacia una estacion.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from integrations.mqtt_config import load_mqtt_config


# Bloque CDLform: funcion/metodo parse_args; encapsula una operacion del flujo del modulo.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publica un mensaje MQTT de prueba.")
    parser.add_argument("--config", default=None, help="Ruta a config/mqtt.json")
    parser.add_argument("--station-id", default=None, help="Estacion destino")
    parser.add_argument("--id-evento", default="manual-test", help="ID de evento de prueba")
    parser.add_argument("--mensaje", default="Prueba manual CDLform MQTT")
    return parser.parse_args()


# Bloque CDLform: funcion/metodo main; encapsula una operacion del flujo del modulo.
def main() -> int:
    args = parse_args()
    config = load_mqtt_config(args.config)

    try:
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise SystemExit(
            "Falta instalar paho-mqtt. Ejecuta: pip install -r requirements.txt"
        ) from exc

    station_id = str(args.station_id or config.station_id).strip()
    topic = f"{config.topic_prefix.strip().strip('/')}/{station_id}/eventos"
    payload = {
        "tipo": "evento_pendiente",
        "id_evento": args.id_evento,
        "estacion": station_id,
        "mensaje": args.mensaje,
        "fecha_publicacion": datetime.now().isoformat(timespec="seconds"),
    }

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if config.username:
        client.username_pw_set(config.username, config.password)

    client.connect(config.broker_host, config.broker_port, keepalive=30)
    result = client.publish(topic, json.dumps(payload, ensure_ascii=False), qos=1)
    result.wait_for_publish(timeout=10)
    client.disconnect()

    print(f"Mensaje publicado en {topic}:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


# Bloque CDLform: punto de ejecucion directa del modulo desde consola.
if __name__ == "__main__":
    raise SystemExit(main())
