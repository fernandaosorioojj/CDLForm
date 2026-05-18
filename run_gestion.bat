@echo off
REM Inicia CDLform en modo gestion.
REM Bloque CDLform: ubica la consola en la carpeta del proyecto.
cd /d %~dp0
set CDLFORM_SQL_PROFILE=gestion
REM Bloque CDLform: ejecuta el proceso Python correspondiente.
python main.py --modo normal
