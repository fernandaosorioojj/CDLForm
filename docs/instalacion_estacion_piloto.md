# Instalacion estacion piloto CDLform

Ultima revision: 2026-05-05

Este documento resume como montar una estacion piloto de CDLform con el modelo MQTT/watchdog. El objetivo es que las estaciones no consulten SQL cada 5 minutos: un watchdog central vigila SQL, publica avisos en Mosquitto y cada estacion reacciona ejecutando `main.py --modo auto`.

## 1. Estructura objetivo

Copiar el proyecto a una ruta estable:

```text
C:\CDLform\
```

No usar Escritorio, Descargas ni carpetas sincronizadas como ubicacion oficial de planta.

## 2. Prerrequisitos

Cada estacion debe tener:

- Python instalado y disponible con `python`.
- Dependencias instaladas desde `requirements.txt`.
- ODBC Driver 18 for SQL Server.
- Acceso de red al SQL Server para el fallback y procesamiento real.
- Acceso de red al broker Mosquitto por TCP 1883.
- `C:\JOBTRACK\jobtrack.ini` configurado con su `Estacao` real.

La maquina central/watchdog debe tener:

- Python y dependencias.
- ODBC Driver 18 for SQL Server.
- Acceso SQL a `eventos_op_pendientes` y `jbt_EstacaoXMaquinas`.
- Acceso al broker Mosquitto.

Instalacion de dependencias:

```bat
cd /d C:\CDLform
python -m pip install -r requirements.txt
```

## 3. Configuracion minima

### SQL

Revisar:

```text
C:\CDLform\config\sql_server.local.json
```

Este archivo es local y no debe versionarse.

Tambien se puede usar `CDLFORM_SQL_CONFIG_PATH` para apuntar a otra ruta. Si se definen variables `CDLFORM_SQL_SERVER`, `CDLFORM_SQL_DATABASE`, `CDLFORM_SQL_USERNAME`, etc., esas variables tienen prioridad sobre el archivo.

### Estacion

Revisar el archivo oficial de JobTrack:

```text
C:\JOBTRACK\jobtrack.ini
```

Debe contener algo como:

```ini
[JOBTRACK]
Estacao=ESTACION-06
idioma=1
```

El listener MQTT usa `station_id: auto`, por lo que detecta la estacion desde este archivo.

Si una estacion piloto no puede usar `C:\JOBTRACK\jobtrack.ini`, definir `CDLFORM_JOBTRACK_INI` apuntando a la ruta alternativa. La plantilla `docs\configuracion\jobtrack.example.ini` sirve para crear ese archivo, pero `config\jobtrack.ini` no es leido por defecto.

### MQTT

Revisar:

```text
C:\CDLform\config\mqtt.json
```

Ejemplo:

```json
{
  "broker_host": "IP_O_DNS_DEL_BROKER",
  "broker_port": 1883,
  "username": "",
  "password": "",
  "station_id": "auto",
  "topic_prefix": "cdlform/estaciones"
}
```

Para el watchdog central, revisar:

```text
C:\CDLform\config\mqtt_watchdog.json
```

Ejemplo:

```json
{
  "poll_interval_seconds": 10,
  "notify_cooldown_seconds": 300,
  "limit": 100
}
```

## 4. Lanzadores estandar

Gestion:

```text
C:\CDLform\run_gestion.bat
```

Listener MQTT por estacion:

```text
C:\CDLform\run_mqtt_listener.bat
```

Watchdog central:

```text
C:\CDLform\run_mqtt_watchdog.bat
```

Fallback/manual operario:

```text
C:\CDLform\run_operario.bat
```

Logs principales:

```text
C:\CDLform\logs\mqtt_station_listener.log
C:\CDLform\logs\mqtt_station_listener_console.log
C:\CDLform\logs\mqtt_sql_watchdog.log
C:\CDLform\logs\mqtt_sql_watchdog_console.log
C:\CDLform\logs\operario_auto.log
```

## 5. Validacion manual MQTT antes de activar servicios/tareas

En una estacion, probar primero sin abrir la app:

```bat
cd /d C:\CDLform
python runtime\mqtt_station_listener.py
```

Debe conectarse al broker y suscribirse al topico de su estacion:

```text
cdlform/estaciones/ESTACION-XX/eventos
```

Desde otra consola, publicar una prueba:

```bat
python runtime\mqtt_publish_test.py --station-id ESTACION-XX --id-evento prueba-001
```

Luego probar con ejecucion real:

```bat
python runtime\mqtt_station_listener.py --run-auto
```

## 6. Validacion del watchdog central

Primero correr sin publicar mensajes:

```bat
cd /d C:\CDLform
python runtime\mqtt_sql_watchdog.py --once --dry-run
```

Validar:

1. que no falle Python;
2. que no falle la conexion SQL;
3. que lea eventos pendientes si existen;
4. que resuelva `CodRecurso -> CodEstacao`;
5. que indique a que topico publicaria.

Despues correr real:

```bat
python runtime\mqtt_sql_watchdog.py
```

## 7. Arranque automatico recomendado

En cada estacion, crear una tarea al iniciar sesion:

- Name: `CDLform MQTT Listener`
- Program/script: `C:\CDLform\run_mqtt_listener.bat`
- Start in: `C:\CDLform`
- Trigger: at log on / al iniciar sesion del usuario
- Recomendado: `Run only when user is logged on` si debe abrir UI visible

En la maquina central, ejecutar el watchdog con:

```text
C:\CDLform\run_mqtt_watchdog.bat
```

Puede quedar como tarea al iniciar Windows o como proceso supervisado por infraestructura.

## 8. Fallback con Task Scheduler

`run_operario.bat` ya no debe ser polling principal cada 5 minutos. Si se mantiene Task Scheduler, usarlo como respaldo:

- Name: `CDLform Operario Fallback`
- Program/script: `C:\CDLform\run_operario.bat`
- Start in: `C:\CDLform`
- Trigger: cada 30 o 60 minutos
- Setting: `Do not start a new instance`

## 9. Checklist rapido

- [ ] App copiada en `C:\CDLform`
- [ ] Python disponible con `python`
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] ODBC Driver 18 instalado
- [ ] `config\sql_server.local.json` validado
- [ ] `C:\JOBTRACK\jobtrack.ini` validado
- [ ] `config\mqtt.json` apunta al broker correcto
- [ ] Broker Mosquitto accesible por TCP 1883
- [ ] `python runtime\mqtt_station_listener.py` probado sin `--run-auto`
- [ ] `python runtime\mqtt_station_listener.py --run-auto` probado
- [ ] `python runtime\mqtt_sql_watchdog.py --once --dry-run` probado
- [ ] `run_mqtt_listener.bat` configurado al inicio de sesion
- [ ] `run_mqtt_watchdog.bat` configurado en maquina central
- [ ] `run_operario.bat` definido solo como fallback
- [ ] prueba con evento real realizada
