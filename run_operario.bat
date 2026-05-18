@echo off
REM Ejecuta el modo automatico de operario, usado por Task Scheduler o fallback.
REM Bloque CDLform: ubica la consola en la carpeta del proyecto.
cd /d %~dp0
set CDLFORM_SQL_PROFILE=operario
REM Bloque CDLform: asegura que exista la carpeta de logs.
if not exist logs mkdir logs
REM Bloque CDLform: ejecuta el proceso Python correspondiente.
python main.py --modo auto >> logs\operario_auto.log 2>&1
