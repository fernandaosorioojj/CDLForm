# Mapa de relevancia del flujo actual

Ultima revision: 2026-05-05

Este documento comenta el rol de los archivos principales del proyecto frente a los flujos vigentes:

- Gestion: administracion, preguntas, reportes, usuarios y dashboard.
- Operario: modo automatico, apertura de formularios y respuesta.
- MQTT piloto: listener por estacion, watchdog SQL central y Mosquitto.
- Soporte/diagnostico: scripts, migraciones y herramientas que no son el camino diario.

## Entradas de ejecucion

| Archivo | Relevancia | Comentario |
| --- | --- | --- |
| `main.py` | Critico | Entrada principal. En `--modo normal` abre login/gestion; en `--modo auto` procesa cola SQL y abre formularios pendientes. |
| `run_gestion.bat` | Critico gestion | Atajo para iniciar la app en modo gestion. |
| `run_operario.bat` | Fallback operario | Atajo para ejecutar `main.py --modo auto` manualmente o como respaldo programado. |
| `runtime\mqtt_station_listener.py` | Critico MQTT piloto | Cliente por estacion. Escucha el topico de su estacion y ejecuta `main.py --modo auto`. |
| `runtime\mqtt_sql_watchdog.py` | Critico MQTT piloto | Proceso central. Consulta `eventos_op_pendientes`, resuelve estacion y publica avisos MQTT. |
| `runtime\mqtt_publish_test.py` | Prueba/diagnostico | Publicador manual para validar Mosquitto y topicos. No forma parte del flujo productivo. |
| `run_mqtt_listener.bat` | Operativo MQTT | Atajo para correr el listener con `--initial-check --run-auto`. |
| `run_mqtt_watchdog.bat` | Operativo MQTT | Atajo para correr el watchdog central. |
| `worker_main.py` | Diagnostico/legado | Herramienta tecnica CLI para procesar eventos. No es el flujo automatico recomendado actual. |

## Configuracion

| Archivo | Relevancia | Comentario |
| --- | --- | --- |
| `config/settings.py` | Critico | Centraliza rutas de datos/configuracion usadas por la app. |
| `config/sql_server_config.py` | Critico | Construye la cadena ODBC hacia SQL Server. Lo usan repositorios, servicios y watchdog. |
| `config/sql_server.local.json` | Critico local | Credenciales y datos SQL locales. No debe versionarse. |
| `C:\JOBTRACK\jobtrack.ini` | Critico estacion | Archivo oficial de estacion usado por defecto para resolver `Estacao`. |
| `config/jobtrack.ini` | Fallback local forzado | Solo aplica si se define `CDLFORM_JOBTRACK_INI` apuntando a esta ruta; no se lee por defecto. |
| `config/mqtt.json` | Critico MQTT local | Config real del broker MQTT y `station_id`. No debe versionarse. |
| `config/mqtt_watchdog.json` | Critico watchdog local | Intervalo, cooldown y limite del watchdog. No debe versionarse. |
| `config/logging_config.py` | Soporte | Configuracion de logging si se usa desde empaquetado/servicios. |
| `config/admin_login.json` / `gestion_login.json` | Critico local | Credenciales locales de app. No deben versionarse. |
| `docs/configuracion/*.example.*` | Plantillas | Archivos guia para crear configs reales sin ensuciar `config/`. |

## Integraciones y lanzamiento

| Archivo | Relevancia | Comentario |
| --- | --- | --- |
| `integrations/event_processor.py` | Critico operario | Fachada del modo automatico. Procesa exclusivamente `eventos_op_pendientes`. |
| `integrations/mqtt_config.py` | Critico MQTT | Lee config MQTT. En estaciones resuelve `station_id=auto` desde `C:\JOBTRACK\jobtrack.ini` u override `CDLFORM_JOBTRACK_INI`. |
| `launcher/app_launcher.py` | Critico UI | Abre ventanas/formularios desde el flujo automatico. |
| `launcher/pending_form_coordinator.py` | Critico operario | Coordina la apertura del siguiente formulario pendiente. |

## Servicios de negocio

| Archivo | Relevancia | Comentario |
| --- | --- | --- |
| `services/workflows/apontamento_procesado_service.py` | Critico operario | Orquesta eventos SQL, omitidos, creacion de formularios y estados. |
| `services/workflows/disparador_service.py` | Critico operario | Reserva formularios en apertura y libera si se cierra sin completar. |
| `services/jobtrack/apontamento_query_service.py` | Critico SQL/JobTrack | Consulta cola SQL, Apontamentos, supervisores y homologacion estacion/recurso. |
| `services/jobtrack/catalogo_contexto_service.py` | Critico contexto | Resuelve recursos de una estacion y catalogos desde SQL. |
| `services/jobtrack/jobtrack_config_service.py` | Critico estacion | Lee la estacion local desde `ini_path` explicito, `CDLFORM_JOBTRACK_INI` o `C:\JOBTRACK\jobtrack.ini`. |
| `services/forms/formulario_service.py` | Critico | Crea, actualiza y lista formularios operario. |
| `services/forms/pregunta_service.py` | Critico gestion | Administra preguntas y reglas de plantilla. |
| `services/forms/plantilla_preguntas_service.py` | Critico gestion/operario | Resuelve plantillas activas por contexto. |
| `services/forms/respuesta_service.py` | Critico operario | Guarda respuestas y validaciones de formulario. |
| `services/reporting/reporte_service.py` | Critico gestion | Alimenta reportes/auditoria. |
| `services/security/auth_service.py` | Critico gestion | Login, hashes y usuarios de gestion. |

## Repositorios y modelos

| Carpeta/archivo | Relevancia | Comentario |
| --- | --- | --- |
| `repositories/base_repository.py` | Legado JSON | Soporte de persistencia JSON antigua; no participa del flujo actual. |
| `repositories/formulario_repository.py` | Critico | Persistencia de formularios operario. |
| `repositories/pregunta_repository.py` | Critico gestion | Persistencia de preguntas. |
| `repositories/plantilla_preguntas_repository.py` | Critico gestion/operario | Persistencia de plantillas. |
| `repositories/respuesta_repository.py` | Critico operario | Persistencia de respuestas. |
| `repositories/usuario_gestion_repository.py` | Critico gestion | Persistencia de usuarios de gestion. |
| `models/*.py` | Critico dominio | Entidades de formulario, pregunta, opciones, plantilla y respuesta. |

## Presenters y UI

| Carpeta/archivo | Relevancia | Comentario |
| --- | --- | --- |
| `presenters/login_presenter.py` | Critico gestion | Coordina login y roles. |
| `presenters/dashboard_gestion_presenter.py` | Critico gestion | KPI y datos de dashboard. |
| `presenters/admin_preguntas_presenter.py` | Critico gestion | Logica de administracion de preguntas/plantillas. |
| `presenters/formulario_operario_presenter.py` | Critico operario | Logica de respuesta/cierre de formulario. |
| `presenters/usuarios_gestion_presenter.py` | Critico gestion | Usuarios de gestion. |
| `ui/login.py` | Critico gestion | Pantalla inicial. |
| `ui/dashboard_gestion.py` | Critico gestion | Panel principal. |
| `ui/admin_preguntas.py` | Critico gestion | ABM de preguntas. |
| `ui/formulario_operario.py` | Critico operario | Pantalla que ve el operario. |
| `ui/detalle_formulario.py` | Critico gestion | Detalle/auditoria de formularios. |
| `ui/reportes.py` | Critico gestion | Reporteria. |
| `ui/acciones_correctivas.py` | Critico gestion | Seguimiento de acciones correctivas. |
| `ui/auditoria_formularios.py` | Critico gestion | Auditoria de formularios/plantillas. |
| `ui/detalle_plantilla_preguntas.py` | Soporte gestion | Vista de detalle de plantilla. |
| `ui/usuarios_gestion.py` | Critico gestion | ABM usuarios. |

## Utilidades, estilos y widgets

| Carpeta/archivo | Relevancia | Comentario |
| --- | --- | --- |
| `core/enums.py` | Soporte dominio | Tipos y estados compartidos. Algunos enums son historicos, pero `TipoPregunta` esta en uso. |
| `core/exceptions.py` | Soporte dominio | Excepciones de dominio. |
| `core/validators.py` | Soporte dominio | Validaciones usadas por modelos/servicios. |
| `utils/assets.py` | Soporte UI | Resuelve rutas de assets. |
| `utils/id_generator.py` | Soporte persistencia | Generacion de IDs correlativos. |
| `utils/json_manager.py` | Soporte legado/local | Utilidad JSON; revisar antes de eliminar porque puede servir a configs antiguas. |
| `utils/style_loader.py` | Critico UI | Carga QSS. |
| `styles/common.py` / `styles/theme.py` | Critico UI | Tema y tokens visuales. |
| `widgets/*.py` | Critico UI | Componentes reutilizables PyQt. |

## Base de datos y documentacion

| Archivo | Relevancia | Comentario |
| --- | --- | --- |
| `database/001_crear_tablas_formularios_operario.sql` | Historico/instalacion | Script base de tablas. No se ejecuta diariamente. |
| `database/001b_agregar_foreign_keys_formularios_operario_dba.sql` | Historico/DBA | Ajustes de FK. Solo DBA/instalacion. |
| `database/006_permitir_estado_en_progreso_formularios_operario.sql` | Instalacion/ajuste | Permite estado `en_progreso` si la DB aun no lo acepta. |
| `database/007_crear_usuarios_gestion.sql` | Instalacion/gestion | Crea o ajusta la tabla `usuarios_gestion`. |
| `docs/guia_tecnica_desarrolladores.md` | Critico conocimiento | Guia tecnica principal. |
| `docs/instalacion_estacion_piloto.md` | Operativo | Instalacion de estaciones. |
| `docs/piloto_mqtt_mosquitto.md` | Critico MQTT piloto | Guia del nuevo flujo MQTT/watchdog. |

## Archivos no criticos para el flujo diario actual

Estos archivos no son irrelevantes en absoluto, pero no participan directamente en la ejecucion diaria gestion/operario/MQTT:

- `worker_main.py`: herramienta tecnica/diagnostico; el flujo recomendado usa `main.py --modo auto`.
- `runtime\mqtt_publish_test.py`: solo prueba manual MQTT; el futuro disparo real viene desde `runtime\mqtt_sql_watchdog.py`.
- `database/*.sql`: instalacion/ajustes SQL; no runtime diario.
- `docs/configuracion/*.example.*`: plantillas, no runtime directo.
- `docs/*`: documentacion, no runtime.
- `utils/json_manager.py`: soporte/local legado; no se ve en el flujo principal inspeccionado.
- En `core/enums.py`, `FormularioEstado`, `DisparadorEstado`, `EventoEstadoProcesamiento` y `OrigenEvento` parecen soporte/historicos; `TipoPregunta` si esta usado.
- `config/logging_config.py`: soporte de logging, no camino principal observado.

## Flujo actual recomendado

### Operario principal con MQTT

```text
runtime\mqtt_sql_watchdog.py
  -> ApontamentoQueryService.listar_eventos_op_pendientes
  -> ApontamentoQueryService.listar_estaciones_por_cod_recursos
  -> Mosquitto
  -> runtime\mqtt_station_listener.py
  -> main.py --modo auto
  -> FormularioOperarioView
```

### Fallback operario con Task Scheduler

```text
run_operario.bat
  -> main.py --modo auto
  -> EventProcessor
  -> ApontamentoProcesadoService.sincronizar_y_crear_formularios_desde_cola_sql
  -> ApontamentoQueryService.listar_eventos_op_pendientes
  -> FormularioService
  -> PendingFormCoordinator
  -> FormularioOperarioView
```

### Gestion

```text
run_gestion.bat / main.py --modo normal
  -> LoginView
  -> presenters
  -> services
  -> repositories
  -> SQL Server
```

