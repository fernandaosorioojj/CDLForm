@echo off
cd /d %~dp0
if not exist logs mkdir logs
python main.py --modo auto >> logs\operario_auto.log 2>&1
