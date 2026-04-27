# Instalacion estacion piloto CDLform

Ultima revision: 2026-04-27

Este documento resume como montar una estacion piloto de CDLform con el modelo actual de despliegue.

## 1. Estructura objetivo

Copiar el proyecto a una ruta estable:

```text
C:\CDLform\
```

No usar Escritorio, Descargas ni carpetas sincronizadas.

## 2. Prerrequisitos

La estacion debe tener:

- Python instalado y disponible con `python`
- dependencias instaladas desde `requirements.txt`
- ODBC Driver 18 for SQL Server
- acceso de red al SQL Server

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

Si se necesita plantilla base, usar:

```text
C:\CDLform\config\sql_server.example.json
```

### Estacion

Revisar:

```text
C:\CDLform\config\jobtrack.ini
```

Si se necesita plantilla base, usar:

```text
C:\CDLform\config\jobtrack.example.ini
```

Lo normal es que este sea el unico archivo que cambie por estacion.

## 4. Lanzadores estandar

Gestion:

```text
C:\CDLform\run_gestion.bat
```

Operario automatico:

```text
C:\CDLform\run_operario.bat
```

El lanzador de operario deja log en:

```text
C:\CDLform\logs\operario_auto.log
```

## 5. Validacion manual antes de Task Scheduler

Primero probar:

```bat
cd /d C:\CDLform
run_operario.bat
```

Validar:

1. que no falle Python
2. que no falle la conexion SQL
3. que detecte la estacion correcta
4. que, si existe evento pendiente, abra el formulario correcto

## 6. Task Scheduler

Crear una tarea por estacion con estos valores:

- Name: `CDLform Operario Auto`
- Program/script: `C:\CDLform\run_operario.bat`
- Start in: `C:\CDLform`
- Trigger: cada 5 minutos
- Setting: `Do not start a new instance`
- Recomendado: `Run only when user is logged on` si debe abrir UI visible

## 7. Checklist rapido

- [ ] App copiada en `C:\CDLform`
- [ ] Python disponible con `python`
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] ODBC Driver 18 instalado
- [ ] `config\sql_server.local.json` validado
- [ ] `config\jobtrack.ini` validado
- [ ] `run_operario.bat` probado manualmente
- [ ] tarea programada creada
- [ ] prueba con evento real realizada
