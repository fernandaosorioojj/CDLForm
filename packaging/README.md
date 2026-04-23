# Empaquetado EXE

Esta carpeta prepara la generacion de ejecutables Windows con PyInstaller.

## Ejecutables objetivo

- `CDLformGestion.exe`: abre login/dashboard gestion.
- `CDLformOperario.exe`: abre modo automatico con UI de operario.
- `CDLformWorker.exe`: procesa cola SQL sin UI para Task Scheduler.

## Requisitos del equipo de build

- Python instalado.
- Dependencias del proyecto instaladas.
- PyInstaller instalado.

Instalacion recomendada desde la raiz del proyecto:

```bat
python -m pip install -r requirements.txt
```

## Generar ejecutables

Desde la raiz del proyecto:

```powershell
.\packaging\build_exe.ps1
```

Salida esperada:

```text
dist\exe\CDLformGestion\
dist\exe\CDLformOperario\
dist\exe\CDLformWorker\
dist\exe\data\
```

Cada carpeta contiene su `.exe` y recursos incluidos. La build ademas prepara una carpeta comun `dist\exe\data\` para configuracion y logs compartidos del despliegue.

## Configuracion local

No se deben empaquetar credenciales productivas dentro del exe.

En cada equipo destino configure:

```text
C:\CDLform\data\sql_server.local.json
C:\CDLform\data\jobtrack.ini
```

La app usa por defecto una carpeta comun `data`:

- En desarrollo: `.\data\`
- En ejecutables: `..\data\` respecto de cada `.exe`

Solo si se define `CDLFORM_DATA_DIR` se usara otra ruta.

Los archivos dentro de `config\` quedan como respaldo de bootstrap/desarrollo, no como ubicacion oficial de produccion.

La build deja ejemplos en:

```text
dist\exe\data\sql_server.example.json
dist\exe\data\jobtrack.example.ini
dist\exe\data\gestion_login.example.json
dist\exe\data\admin_login.example.json
```

## Task Scheduler

Para la tarea programada use `CDLformWorker.exe`.

Ejemplo:

```text
Program/script:
C:\CDLform\CDLformWorker\CDLformWorker.exe

Start in:
C:\CDLform\CDLformWorker
```

Si se requiere log, apunte Task Scheduler a un `.bat` que ejecute el exe y redirija salida:

```bat
@echo off
cd /d C:\CDLform\CDLformWorker
if not exist ..\data mkdir ..\data
if not exist ..\data\logs mkdir ..\data\logs
CDLformWorker.exe >> ..\data\logs\worker.log 2>&1
```
