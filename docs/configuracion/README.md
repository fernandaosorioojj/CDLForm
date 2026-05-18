# Plantillas de configuracion

Ultima revision: 2026-05-05

Esta carpeta guarda ejemplos de archivos locales que no forman parte directa del runtime.

La carpeta `config/` debe quedar reservada para configuracion real de la aplicacion y modulos Python. Para instalar una estacion o una maquina central, copia la plantilla necesaria desde esta carpeta hacia `config/` y renombrala sin `.example`.

| Plantilla | Copiar como | Uso |
| --- | --- | --- |
| `admin_login.example.json` | `config/admin_login.json` | Fallback local de login admin. |
| `gestion_login.example.json` | `config/gestion_login.json` | Fallback local de login gestion. |
| `jobtrack.example.ini` | `C:\JOBTRACK\jobtrack.ini` o ruta definida por `CDLFORM_JOBTRACK_INI` | Estacion local. El codigo no lee `config/jobtrack.ini` por defecto. |
| `mqtt.example.json` | `config/mqtt.json` | Conexion de listener/watchdog al broker MQTT. |
| `mqtt_watchdog.example.json` | `config/mqtt_watchdog.json` | Intervalos y limites del watchdog SQL -> MQTT. |
| `sql_server.local.example.json` | `config/sql_server.local.json` | Conexion SQL local. No usar credenciales reales en la plantilla. |
