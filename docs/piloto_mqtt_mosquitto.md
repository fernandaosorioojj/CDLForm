# Piloto MQTT con Mosquitto

Ultima revision: 2026-05-05

Este piloto valida primero el canal MQTT aislado y luego el watchdog SQL central, sin cambiar la regla principal: SQL Server sigue siendo la fuente de verdad y MQTT solo despierta estaciones.

En este piloto, Mosquitto se aloja en el PC de desarrollo:

```text
Broker MQTT: 172.16.10.247:1883
```

## Flujo objetivo

```text
SQL Server eventos_op_pendientes
  -> runtime\mqtt_sql_watchdog.py
  -> Mosquitto
  -> runtime\mqtt_station_listener.py en la estacion
  -> main.py --modo auto
```

SQL Server sigue siendo la fuente de verdad. MQTT solo despierta estaciones.

## Objetivo del piloto manual

Probar esta ruta:

```text
runtime\mqtt_publish_test.py -> Mosquitto -> runtime\mqtt_station_listener.py
```

Luego, cuando el canal sea confiable, se puede conectar un watchdog SQL a `eventos_op_pendientes`.

## 1. Instalar dependencia Python

```bat
pip install -r requirements.txt
```

## 2. Crear configuracion local

Copiar:

```text
docs/configuracion/mqtt.example.json
```

como:

```text
config/mqtt.json
```

Ajustar:

```json
{
  "broker_host": "172.16.10.247",
  "broker_port": 1883,
  "username": "",
  "password": "",
  "station_id": "auto",
  "topic_prefix": "cdlform/estaciones"
}
```

Con `"station_id": "auto"`, el listener lee la estacion desde el mismo archivo oficial que usa la app:

```text
C:\JOBTRACK\jobtrack.ini
```

Si se necesita forzar una estacion para una prueba, se puede reemplazar `auto` por un valor fijo como `ESTACION-06`.

Si el piloto necesita una ruta alternativa para JobTrack, definir `CDLFORM_JOBTRACK_INI`. La app no lee `config\jobtrack.ini` por defecto.

Si la IP del PC que aloja Mosquitto cambia, revisar con:

```bat
ipconfig
```

y actualizar `broker_host` en `config/mqtt.json`.

## 2.1 Mantener Mosquitto corriendo en este PC

En el PC broker:

```bat
cd "C:\Program Files\mosquitto"
mosquitto.exe -v
```

Las otras estaciones deben poder alcanzar el puerto TCP `1883` de este PC.

## 3. Ejecutar listener en la estacion

Modo seguro, solo registra mensajes:

```bat
python runtime\mqtt_station_listener.py
```

El log queda en:

```text
logs/mqtt_station_listener.log
```

## 4. Publicar mensaje manual

Desde el servidor o desde otra consola:

```bat
python runtime\mqtt_publish_test.py --id-evento prueba-001
```

Si todo esta correcto, el listener debe mostrar y registrar el mensaje.

Para publicar a una estacion especifica:

```bat
python runtime\mqtt_publish_test.py --station-id ESTACION-06 --id-evento prueba-001
```

## 5. Prueba opcional ejecutando la app

Solo cuando el canal MQTT manual ya este validado:

```bat
python runtime\mqtt_station_listener.py --run-auto
```

Con `--run-auto`, cada mensaje MQTT ejecuta:

```bat
python main.py --modo auto
```

Para cubrir eventos ocurridos mientras la estacion estaba apagada:

```bat
python runtime\mqtt_station_listener.py --initial-check --run-auto
```

Para dejar el listener corriendo con el modo recomendado de piloto:

```bat
run_mqtt_listener.bat
```

## 6. Watchdog SQL central

El watchdog se ejecuta solo en la maquina central que vigila SQL y publica MQTT.

Configurar:

```text
config/mqtt_watchdog.json
```

Ejemplo:

```json
{
  "poll_interval_seconds": 10,
  "notify_cooldown_seconds": 300,
  "limit": 100
}
```

Significado:

```text
poll_interval_seconds: cada cuantos segundos consulta eventos_op_pendientes
notify_cooldown_seconds: tiempo minimo antes de repetir aviso del mismo id_evento
limit: maximo de eventos pendientes consultados por ciclo
```

Prueba segura sin publicar MQTT:

```bat
python runtime\mqtt_sql_watchdog.py --once --dry-run
```

Ejecucion real:

```bat
python runtime\mqtt_sql_watchdog.py
```

O con el .bat:

```bat
run_mqtt_watchdog.bat
```

El watchdog no marca eventos como procesados. Solo publica avisos. El procesamiento sigue ocurriendo en `main.py --modo auto`.

## Regla de diseno

MQTT es solo la campana de aviso. La verdad persistente sigue siendo SQL Server:

```text
eventos_op_pendientes = evento real
MQTT = aviso rapido
main.py --modo auto = procesamiento actual
```

