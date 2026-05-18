@echo off
REM Inicia el watchdog central que publica avisos MQTT desde SQL.
REM Bloque CDLform: ubica la consola en la carpeta del proyecto.
cd /d %~dp0
set CDLFORM_SQL_PROFILE=watchdog
REM Bloque CDLform: asegura que exista la carpeta de logs.
if not exist logs mkdir logs
REM Bloque CDLform: ejecuta el proceso Python correspondiente.
python runtime\mqtt_sql_watchdog.py >> logs\mqtt_sql_watchdog_console.log 2>&1
