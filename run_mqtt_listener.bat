@echo off
REM Inicia el listener MQTT de estacion con revision inicial y ejecucion automatica.
REM Bloque CDLform: ubica la consola en la carpeta del proyecto.
cd /d %~dp0
set CDLFORM_SQL_PROFILE=operario
REM Bloque CDLform: asegura que exista la carpeta de logs.
if not exist logs mkdir logs
REM Bloque CDLform: ejecuta el proceso Python correspondiente.
python runtime\mqtt_station_listener.py --initial-check --run-auto >> logs\mqtt_station_listener_console.log 2>&1
