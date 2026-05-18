# Guia tecnica para desarrolladores CDLform

Ultima revision: 2026-05-05

Este documento describe como esta organizada la aplicacion, como viajan los datos por el flujo actual y que archivos son relevantes para mantenimiento. Esta escrito para que un desarrollador nuevo pueda modificar el sistema sin romper integraciones con SQL Server, Apontamentos o la UI PyQt.

## 1. Vision general

CDLform es una aplicacion PyQt orientada a dos superficies:

- Gestion: login, dashboard, administracion de preguntas, reportes, acciones correctivas, auditoria y administracion de usuarios.
- Operario: apertura automatica de formularios generados desde Apontamentos/eventos SQL, respuesta de preguntas y envio final.

El flujo actual asume que el operario y supervisor vienen desde Apontamentos. Ya no existe seleccion manual de operario dentro de la aplicacion.

Capas principales:

- `ui/`: widgets y ventanas PyQt.
- `presenters/`: coordinan validaciones y adaptan servicios a la UI.
- `services/`: reglas de negocio, integracion de datos y flujos.
- `repositories/`: persistencia SQL Server vigente; la ruta JSON queda como legado tecnico documentado.
- `models/`: modelos de dominio serializables.
- `integrations/` y `launcher/`: entrada automatica, procesamiento y apertura de formularios.
- `database/`: scripts historicos/migraciones SQL.
- `config/`, `styles/`, `utils/`, `widgets/`: soporte transversal.

## 2. Flujo de ejecucion

### 2.1 Modo gestion

Entrada:

```text
main.py --modo normal
```

Secuencia:

```text
main.py
  -> QApplication
  -> LoginView
  -> LoginPresenter
  -> AuthService
  -> UsuarioGestionRepository o fallback JSON/env
  -> DashboardGestionView
  -> vistas de gestion
```

Puntos importantes:

- `AuthService` intenta autenticar contra SQL en `[dbo].[usuarios_gestion]`.
- Si SQL no responde o no encuentra el usuario, usa fallback por variables de entorno o archivos JSON.
- Si el login fallback es exitoso, intenta sincronizar ese usuario hacia SQL.
- Los roles validos son `admin` y `gestion`.
- Solo `admin` deberia ver administracion de usuarios.

Riesgos:

- Si el usuario SQL de la app no tiene permisos para crear/leer `usuarios_gestion`, login puede caer a fallback y ocultar un problema de permisos.
- El fallback JSON/env es util para continuidad, pero puede generar confusion si SQL esta vacio.
- Los hashes son PBKDF2; nunca guardar password plano.

### 2.2 Modo automatico con UI operario

Entrada:

```text
main.py --modo auto
```

Secuencia:

```text
main.py
  -> EventProcessor
  -> ApontamentoProcesadoService
  -> ApontamentoQueryService
  -> eventos_op_pendientes
  -> FormularioService
  -> FormularioRepository
  -> PendingFormCoordinator
  -> DisparadorService
  -> AppLauncher
  -> FormularioOperarioView
```

Comportamiento:

- Sincroniza solamente desde `[dbo].[eventos_op_pendientes]`.
- La consulta directa a `[dbo].[Apontamentos]` no forma parte del flujo productivo automatico; queda documentada como respaldo de emergencia para uso tecnico/manual.
- Crea formularios en estado `en_apertura`.
- `PendingFormCoordinator` abre el siguiente formulario pendiente.
- `AppLauncher` abre directamente `FormularioOperarioView`; no existe pantalla intermedia para seleccionar operario.

Riesgos:

- Eventos sin `num_ordem` se omiten y se marcan con mensaje.
- Formularios ya completados se omiten para no reprocesar.
- Si falta plantilla activa para `CodSetor` + `CodRecurso`, no se crea formulario.
- Si el estado `en_progreso` no esta permitido por constraint SQL, `FormularioService` intenta compatibilidad temporal volviendo a `pendiente_operario`.

### 2.3 Flujo MQTT/watchdog operario

Entrada central:

```text
runtime\mqtt_sql_watchdog.py
```

Entrada por estacion:

```text
runtime\mqtt_station_listener.py --initial-check --run-auto
```

Secuencia:

```text
eventos_op_pendientes
  -> runtime\mqtt_sql_watchdog.py
  -> Mosquitto
  -> runtime\mqtt_station_listener.py
  -> main.py --modo auto
  -> FormularioOperarioView
```

Uso esperado:

- El watchdog corre en una sola maquina central y consulta SQL con intervalo/cooldown controlado.
- Mosquitto solo reparte avisos; no guarda la verdad del negocio.
- Cada estacion mantiene un listener MQTT y ejecuta `main.py --modo auto` cuando recibe aviso.
- `run_operario.bat` queda como fallback manual o programado con baja frecuencia, no como polling principal cada 5 minutos.

Riesgos:

- Si Mosquitto no escucha en red o el firewall bloquea TCP 1883, las estaciones no reciben avisos.
- Si el watchdog no puede conectar a SQL, no publicara eventos aunque la app local siga funcionando manualmente.
- Si una estacion estaba apagada, `--initial-check` y el fallback periodico recuperan pendientes persistidos en SQL.

### 2.4 Worker tecnico de diagnostico

Entrada:

```text
worker_main.py
```

Uso esperado:

- Herramienta tecnica para ejecutar el procesador desde consola y revisar JSON de resultado.
- No es la pieza principal de despliegue de operario porque no administra el listener MQTT ni la apertura visible como flujo residente.

## 3. Estados del formulario

Estados principales:

- `pendiente_operario`: formulario listo para abrir.
- `en_apertura`: reservado por el launcher para evitar doble apertura.
- `en_progreso`: operario ya abrio el formulario.
- `completado`: formulario respondido/enviado.
- `cancelado`: cierre administrativo o flujo cancelado.

Transiciones relevantes:

```text
evento/apontamento -> en_apertura
en_apertura -> en_progreso al cargar FormularioOperarioView
en_progreso -> completado al enviar respuestas
en_apertura -> pendiente_operario si se cierra la ventana antes de avanzar
```

Riesgos:

- Si una ventana cae antes de liberar correctamente, un formulario podria quedar en `en_apertura`.
- Si la DB no tiene el script de estado `en_progreso`, puede haber fallback a `pendiente_operario`.
- La carga de pendientes se ordena por `fecha_creacion` e `id_formulario`.

## 4. Revision por archivo

### Raiz

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `.gitignore` | Controla archivos excluidos del versionado. | Mantener fuera credenciales, caches y configs locales sensibles. |
| `main.py` | Entrada principal de la app PyQt. Maneja modo `normal` y `auto`. | Cambios aqui afectan arranque completo. Validar que no bloquee `QApplication` ni rompa apertura automatica. |
| `requirements.txt` | Dependencias Python vigentes. | Incluye `paho-mqtt`; si falta, listener/watchdog MQTT no arrancan. |
| `run_gestion.bat` | Lanzador de gestion. | Debe ejecutarse desde la carpeta del proyecto para resolver rutas relativas. |
| `run_operario.bat` | Lanzador fallback/manual de modo auto. | Es respaldo operativo; no debe volver a ser polling principal cada 5 minutos. |
| `run_mqtt_listener.bat` | Lanzador del listener por estacion. | Debe correr con usuario Windows que pueda abrir UI visible. |
| `run_mqtt_watchdog.bat` | Lanzador del watchdog central. | Debe correr solo en maquina central/broker con acceso SQL. |
| `worker_main.py` | Entrada tecnica de diagnostico sin UI. | No es el flujo principal de operario; usar para pruebas controladas. |

### `assets/images`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `cdl-logo.svg` | Logo usado por login. | Si cambia nombre, actualizar `ui/login.py`. |
| `icon-audit.svg` | Icono de auditoria en dashboard. | Usado por `AssetImage`; ruta por nombre. |
| `icon-corrective.svg` | Icono de acciones correctivas. | Mantener nombre estable o actualizar dashboard. |
| `icon-questions.svg` | Icono de preguntas. | Mantener formato SVG compatible con Qt. |
| `icon-reports.svg` | Icono de reportes/inicio. | Tambien se usa en navegacion. |
| `leaf-accent.svg` | Visual decorativo del dashboard. | Si se elimina, dashboard queda con imagen faltante. |
| `operator-illustration.svg` | Ilustracion de login. | Referenciada por `ui/login.py`. |
| `workflow-illustration.svg` | Ilustracion de dashboard. | Referenciada por `ui/dashboard_gestion.py`. |

### `config`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `admin_login.json` | Fallback legacy de login. | Puede ocultar falta de usuarios SQL. Revisar si se mantiene por continuidad. |
| `gestion_login.json` | Fallback actual de login. | Sensible; idealmente migrar a SQL y restringir acceso. |
| `jobtrack.ini` | Fallback local forzado de estacion JobTrack. | No se lee por defecto; usar solo si `CDLFORM_JOBTRACK_INI` apunta a este archivo. |
| `logging_config.py` | Configura logging rotativo. | Revisar permisos de escritura en directorio de logs. |
| `mqtt.json` | Configuracion local de broker/listener MQTT. | No versionar credenciales ni IPs sensibles; usar plantilla en `docs/configuracion`. |
| `mqtt_watchdog.json` | Configuracion local del watchdog SQL -> MQTT. | Controla intervalo, cooldown y limite; no debe versionarse. |
| `settings.py` | Define rutas, entorno, timezone y paths de configuracion. | Cambios aqui afectan app congelada, desarrollo y el estandar `data` del despliegue. |
| `sql_server.local.json` | Configuracion local SQL. | Sensible; si apunta a DB equivocada, toda la app opera en otro ambiente. |
| `sql_server_config.py` | Construye connection string desde env/config. | Punto critico para errores ODBC, cifrado, permisos y ambiente. |
| `__init__.py` | Paquete Python. | Sin logica. |

Las plantillas de configuracion viven en `docs/configuracion/` para no mezclarlas con archivos reales de runtime.

### `core`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `enums.py` | Enumeraciones de estados/tipos/origen. | Hay constantes similares en `models/formulario.py`; evitar duplicar sin sincronizar. |
| `exceptions.py` | Excepciones de dominio. | Usadas por validadores y servicios. |
| `validators.py` | Validaciones transversales. | Cambios pueden romper modelos que validan datos. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `database`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `001_crear_tablas_formularios_operario.sql` | Script base de tablas de formularios. | Ejecutar en DB correcta; revisar constraints antes de reprocesar. |
| `001b_agregar_foreign_keys_formularios_operario_dba.sql` | Ajustes de FK para DBA. | Requiere permisos; puede fallar si datos historicos no cumplen. |
| `006_permitir_estado_en_progreso_formularios_operario.sql` | Permite estado `en_progreso`. | Si falta, la app usa compatibilidad parcial. Ejecutar con DBA si constraint falla. |
| `007_crear_usuarios_gestion.sql` | Crea/ajusta `usuarios_gestion`. | Debe ejecutarse en `MetricsBetaProductivo` u otra DB objetivo correcta. |

Las migraciones de datos de prueba `002` a `005` fueron eliminadas porque no tienen valor para el flujo actual ni para planta.

### `integrations`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `event_processor.py` | Fachada de procesamiento externo. Procesa exclusivamente la cola SQL productiva. | Si se reintroduce consulta directa a Apontamentos, debe quedar como emergencia controlada y no como fallback automatico. |
| `mqtt_config.py` | Carga config MQTT y resuelve topicos por estacion. | `station_id=auto` depende de JobTrack; si falla estacion, no hay suscripcion valida. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `runtime`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `mqtt_station_listener.py` | Listener MQTT por estacion. | Mantiene proceso residente, escucha topico de la estacion y lanza `main.py --modo auto`. |
| `mqtt_sql_watchdog.py` | Watchdog central SQL -> MQTT. | Consulta eventos pendientes y publica avisos; no marca eventos como procesados. |
| `mqtt_publish_test.py` | Publicador manual de prueba. | Solo diagnostico del canal MQTT; no usar como integracion productiva. |

### `launcher`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `app_launcher.py` | Crea/abre `FormularioOperarioView`. Mantiene ventanas abiertas. | Punto critico: ya no debe importar seleccion manual de operario. |
| `pending_form_coordinator.py` | Timer/coordinador de pendientes. Evita abrir doble ventana. | Si falla liberacion, puede dejar estados en apertura. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `models`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `formulario.py` | Modelo central del formulario y estados. | Cualquier campo nuevo debe mapearse tambien en repository/service/UI. |
| `opcion_pregunta.py` | Modelo de opcion de respuesta. | Acciones correctivas dependen de `accion_correctiva`. |
| `plantilla_preguntas.py` | Modelos de versionado de plantillas. | Cambios afectan historial y auditoria. |
| `pregunta.py` | Modelo de pregunta con opciones y validaciones. | Cuidar `orden`, `tipo`, `obligatoria` y opciones. |
| `respuesta.py` | Modelo de respuesta del operario. | Debe mantenerse compatible con tipos de pregunta. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `presenters`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `admin_preguntas_presenter.py` | Logica de administracion de preguntas/plantillas. | Riesgo alto: versionado, historial y opciones se coordinan aqui. |
| `dashboard_gestion_presenter.py` | Fabrica vistas del dashboard y entrega metricas. | Si se agrega vista, registrar aqui y en dashboard. |
| `formulario_operario_presenter.py` | Prepara formulario, preguntas, validaciones y guardado de respuestas. | Punto critico del flujo operario; no debe reparar plantillas automaticamente al responder. |
| `login_presenter.py` | Envuelve autenticacion para UI. | Mantener retorno de usuario/rol consistente. |
| `usuarios_gestion_presenter.py` | Logica de ABM de usuarios de gestion. | No permitir rol supervisor; solo `admin` y `gestion`. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `repositories`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `base_repository.py` | Repositorio JSON generico legado. | No participa del flujo actual; no usar para produccion. |
| `formulario_repository.py` | Persistencia de formularios en SQL Server. | Mapeo critico de columnas: operador/supervisor/plantilla/estado. La ruta JSON interna es legacy. |
| `plantilla_preguntas_repository.py` | Persistencia de plantillas/versiones. | Riesgo de activar multiples versiones si no se controla. |
| `pregunta_repository.py` | Persistencia SQL de preguntas y opciones. | `filtros_contexto_json` es una columna SQL; la ruta JSON de archivo es legacy. |
| `respuesta_repository.py` | Persistencia SQL de respuestas. | Riesgo de duplicados si se guarda dos veces el mismo formulario. La ruta JSON interna es legacy. |
| `usuario_gestion_repository.py` | Persistencia SQL de usuarios gestion. | Requiere permisos CREATE/SELECT/UPDATE en DB objetivo. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `services/forms`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `formulario_service.py` | Regla central para crear, actualizar estados y completar formularios. | Depende de plantilla activa y datos base del apontamento. |
| `plantilla_preguntas_service.py` | Versionado y busqueda de plantilla activa por contexto. | Cuidar desactivacion/version nueva al editar. |
| `pregunta_service.py` | CRUD/logica de preguntas. | Cambios afectan admin y formulario operario. |
| `respuesta_service.py` | Crea/lista respuestas. | Validaciones de tipo/opcion obligatoria deben estar sincronizadas con UI. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `services/jobtrack`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `apontamento_query_service.py` | Consulta Apontamentos, eventos pendientes, supervisores y contexto SQL. | Mayor superficie de errores SQL: permisos, columnas, drivers, datos dummy. |
| `catalogo_contexto_service.py` | Resuelve estacion/recursos y placeholders SQL. | Si mapeo estacion-recursos falla, no se encuentran eventos. |
| `jobtrack_config_service.py` | Lee estacion local desde config. | Config local incorrecta deja el flujo sin recursos. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `services/reporting`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `reporte_service.py` | Construye dashboard, reportes, auditoria y acciones correctivas. | Hoy lista datos desde servicios; si crece volumen, conviene paginar en SQL, no solo UI. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `services/security`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `auth_service.py` | Login, hashing, roles y fallback. | No relajar validacion de hash. Mantener roles cerrados. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `services/workflows`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `apontamento_procesado_service.py` | Orquesta eventos/apontamentos y creacion de formularios. | Punto clave para reprocesos, omitidos y errores por datos incompletos. |
| `disparador_service.py` | Selecciona y reserva formularios pendientes para abrir. | Maneja set en memoria; no resuelve concurrencia entre procesos distintos. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `styles`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `acciones_correctivas.qss` | Estilos de acciones correctivas. | Mantener objectName/property usados por UI. |
| `admin_preguntas.qss` | Estilos de flujo admin preguntas. | Cambios pueden afectar tabs/fases/resumen. |
| `auditoria_formularios.qss` | Estilos auditoria. | Revisar tablas/paginacion. |
| `base.qss` | Estilo base comun. | Impacto global. Probar login, dashboard y operario. |
| `common.py` | Helper para aplicar QSS. | Depende de `utils/style_loader.py`. |
| `dashboard_gestion.qss` | Estilos dashboard. | Impacto en navegacion y cards. |
| `detalle_formulario.qss` | Estilos detalle modal/formulario. | Usado por `ui/detalle_formulario.py`. |
| `detalle_plantilla_preguntas.qss` | Estilos detalle plantilla. | Usado por auditoria. |
| `dialogs.qss` | Estilos de dialogos. | Usado por confirmaciones y detalles. |
| `formulario_operario.qss` | Estilos formulario operario. | Validar legibilidad en pantalla de planta. |
| `login.qss` | Estilos login. | Probar con errores y textos largos. |
| `reportes.qss` | Estilos reportes. | Paginacion y tablas dependen de objectName. |
| `theme.py` | Tokens de color/tipografia. | Cambios impactan todos los QSS con variables. |
| `usuarios_gestion.qss` | Estilos administracion usuarios. | Solo visible para admin. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `ui`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `acciones_correctivas.py` | Vista de acciones correctivas con paginacion. | Datos vienen de `ReporteService`; supervisor puede venir guardado o SQL. |
| `admin_preguntas.py` | Flujo de 4 fases para crear/editar preguntas: datos, contexto, opciones, resumen. | Guardado solo al final; cualquier cambio debe respetar orden y versionado. |
| `auditoria_formularios.py` | Vista de auditoria de formularios/plantillas. | Cuidar performance: paginacion UI no reduce consulta SQL. |
| `dashboard_gestion.py` | Vista principal gestion y navegacion. | Controla visibilidad de usuarios por rol. |
| `detalle_formulario.py` | Detalle de formulario/respuestas. | Se usa desde reportes y acciones. |
| `detalle_plantilla_preguntas.py` | Detalle de version de plantilla/preguntas. | Importante para auditoria historica. |
| `formulario_operario.py` | Vista operario final. Renderiza preguntas, valida y envia respuestas. | No debe pedir seleccion manual de operario; usa datos del formulario/apontamento. |
| `login.py` | Vista de login. | Debe propagar `usuario` y `rol` al dashboard. |
| `reportes.py` | Vista reportes con filtros y paginacion UI. | Si crece el volumen, mover paginacion al service/repository. |
| `usuarios_gestion.py` | ABM de usuarios gestion. | No crear supervisores; supervisores vienen de Apontamentos. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `utils`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `assets.py` | Resuelve rutas de imagenes. | Si cambia estructura assets, actualizar aqui. |
| `id_generator.py` | Generacion de IDs. | Evitar colisiones con IDs generados por repositorios. |
| `json_manager.py` | Lectura/escritura JSON. | Usado por fallback; puede sobrescribir si estructura cambia. |
| `style_loader.py` | Carga QSS y reemplaza tokens de theme. | Si falta QSS, lo omite silenciosamente. |
| `__init__.py` | Paquete Python. | Sin logica. |

### `widgets`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `asset_image.py` | Widget para renderizar SVG/imagenes. | Si imagen falta, puede afectar layout visual. |
| `base_window.py` | Ventana base con gradiente/estilo comun. | Impacto en vistas que heredan de ella. |
| `card_frame.py` | Frame con propiedad `card=true`. | Usado por login y otras tarjetas. |
| `__init__.py` | Paquete Python. | Sin logica. |

## 5. Puntos tecnicos donde suelen aparecer errores

### Conexion SQL

Origen:

- `config/sql_server_config.py`
- `config/sql_server.local.json`
- ruta local de datos de la app
- Variables de entorno
- Driver ODBC instalado

Sintomas:

- Error SSL/cifrado.
- Login no aparece en SQL.
- La app opera contra otra base.
- No se crean tablas por falta de permisos.

Recomendacion:

- Confirmar DB activa antes de ejecutar scripts.
- Validar `SUSER_SNAME()`, `USER_NAME()` y `ORIGINAL_LOGIN()` con DBA.
- Mantener configuracion local fuera de commits reales.

### Apontamentos y eventos

Origen:

- `[dbo].[eventos_op_pendientes]`
- `[dbo].[Apontamentos]`
- `[dbo].[jbt_EstacaoXMaquinas]`

Errores frecuentes:

- `NumOrdem` vacio.
- `CodRecurso` o `CodSetor` sin plantilla activa.
- `HoraFim` dummy o no finalizada.
- Supervisor existe en Apontamentos pero el evento ya fue procesado antes de que la app lo trajera.
- Estacion local sin recursos homologados.

### Plantillas y preguntas

Errores frecuentes:

- Editar pregunta activa sin versionar correctamente.
- Guardar opciones sin accion correctiva esperada.
- Cambiar orden y romper lectura historica.
- Formulario creado sin `id_plantilla_preguntas`.

Regla importante:

- El formulario debe responder contra la plantilla/version asignada al momento de creacion, no contra la plantilla activa futura.

### Reportes y auditoria

Riesgo actual:

- Las vistas paginan 100 registros en UI, pero los services siguen trayendo colecciones completas.

Escalamiento recomendado:

- Agregar paginacion SQL (`OFFSET/FETCH` o `TOP` + cursor por fecha/id) en repositories/services cuando el volumen crezca.

### Autenticacion

Riesgos:

- Fallback JSON/env puede confundir si la tabla SQL esta vacia.
- `ensure_schema()` intenta crear tabla; requiere permisos.
- Roles fuera de `admin`/`gestion` se normalizan a `gestion`.

## 6. Reglas para futuros cambios

- No reintroducir seleccion manual de operario. Operario y supervisor vienen de Apontamentos.
- Si se agrega un campo a formulario, actualizar modelo, repository, service, UI, reportes y scripts SQL.
- Si se agrega una vista de gestion, registrar presenter/dashboard/styles.
- Si se cambia un estado, actualizar constants, constraints SQL, filtros de pendientes, reportes y dashboard.
- Si se modifica admin de preguntas, conservar guardado final y resumen posterior a opciones.
- No guardar passwords planos. Usar `AuthService.generar_password_hash`.
- Antes de cambiar queries SQL, probar en ambiente correcto y con usuario de la app.

## 7. Validacion recomendada sin tests automatizados

Como los archivos de test fueron eliminados, la validacion manual minima deberia cubrir:

1. Login con usuario `admin`.
2. Login con usuario `gestion`.
3. Dashboard sin vista Usuarios para `gestion`.
4. Crear pregunta nueva con flujo de 4 fases.
5. Editar pregunta y enviar a historial.
6. Procesar evento desde `worker_main.py`.
7. Abrir `main.py --modo auto` y verificar formulario operario directo.
8. Enviar formulario con respuesta que tenga accion correctiva.
9. Revisar reportes, auditoria y acciones correctivas.
10. Verificar que supervisor aparece cuando viene desde Apontamentos.

## 8. Despliegue y distribucion

Esta seccion describe como deberia instalarse y operarse CDLform en una estacion o equipo de gestion. Hoy la referencia valida del proyecto es ejecucion desde codigo fuente con Python, no empaquetado EXE.

### 8.0 Modelo unico de release

El modelo unico recomendado para planta es este:

```text
C:\CDLform\
  main.py
  runtime\mqtt_station_listener.py
  runtime\mqtt_sql_watchdog.py
  worker_main.py
  assets\
  config\
  database\
  docs\
  integrations\
  launcher\
  models\
  presenters\
  repositories\
  services\
  styles\
  ui\
  utils\
  widgets\
  run_gestion.bat
  run_operario.bat
  run_mqtt_listener.bat
  run_mqtt_watchdog.bat
  logs\
```

Regla de distribucion:

- El contenido de la aplicacion es igual para todos los computadores.
- La configuracion SQL puede ser igual para todos si todas las estaciones apuntan al mismo ambiente.
- El unico archivo que normalmente cambia por estacion es `C:\JOBTRACK\jobtrack.ini` o la ruta definida por `CDLFORM_JOBTRACK_INI`.
- Gestion se abre manualmente.
- Operario corre con listener MQTT por estacion; Task Scheduler queda como fallback.

Archivos operativos estandar:

`run_gestion.bat`

```bat
@echo off
cd /d C:\CDLform
python main.py --modo normal
```

`run_operario.bat`

```bat
@echo off
cd /d C:\CDLform
if not exist logs mkdir logs
python main.py --modo auto >> logs\operario_auto.log 2>&1
```

Objetivo del modelo:

- evitar diferencias innecesarias entre estaciones
- dejar un solo punto de configuracion por equipo
- facilitar soporte
- permitir replicacion simple a toda la planta

### 8.1 Conceptos clave

Hay dos superficies operativas:

| Superficie | Comando | Para que sirve |
| --- | --- | --- |
| Gestion | `python main.py --modo normal` | Abre login, dashboard, administracion, reportes, auditoria y usuarios. |
| Operario automatico | `python main.py --modo auto` | Consulta la cola SQL de la estacion y abre el formulario si corresponde. |

Adicionalmente existe `worker_main.py` como herramienta tecnica sin UI, pero no debe considerarse la pieza principal del despliegue de operario. El flujo principal recomendado es listener MQTT por estacion + watchdog central; `run_operario.bat` queda como fallback.

Lo importante es que el usuario Windows que ejecute la app tenga:

- Python instalado.
- Dependencias instaladas (`PyQt5`, `pyodbc`, etc.).
- Driver ODBC compatible.
- Acceso a SQL Server.
- Configuracion local correcta.
- Permisos de escritura en la ruta local de datos/logs.

### 8.2 Que se debe hacer manualmente

Antes de dejar una estacion operativa, hay pasos manuales que no conviene automatizar a ciegas:

1. Copiar o desplegar la carpeta release `C:\CDLform` en el equipo destino.
2. Confirmar que Python y dependencias funcionan.
3. Instalar/verificar driver ODBC de SQL Server.
4. Configurar conexion SQL del ambiente correcto.
5. Configurar estacion Jobtrack del equipo.
6. Ejecutar scripts SQL pendientes en la base correcta con DBA si aplica.
7. Crear o validar usuario administrador de gestion.
8. Crear acceso directo para gestion si se usara en ese equipo.
9. Crear tarea programada en cada estacion de operario.
10. Ejecutar checklist de validacion.

### 8.3 Estructura recomendada en el equipo destino

La estructura objetivo para todas las estaciones debe ser:

```text
C:\CDLform\
  main.py
  runtime\mqtt_station_listener.py
  runtime\mqtt_sql_watchdog.py
  worker_main.py
  assets\
  config\
  database\
  docs\
  integrations\
  launcher\
  models\
  presenters\
  repositories\
  services\
  styles\
  ui\
  utils\
  widgets\
  run_gestion.bat
  run_operario.bat
  run_mqtt_listener.bat
  run_mqtt_watchdog.bat
  logs\
```

Para produccion es preferible una ruta estable como `C:\CDLform` o `C:\Aplicaciones\CDLform`, porque Task Scheduler y accesos directos quedan menos fragiles.

No usar Escritorio, Descargas ni carpetas sincronizadas como ubicacion oficial de planta.

### 8.4 Configuracion SQL

La conexion se arma en `config/sql_server_config.py`.

Rutas de archivo consideradas:

1. Variable `CDLFORM_SQL_CONFIG_PATH`, si existe.
2. Archivo local en ruta de datos de la app (`%APPDATA%\CDLform\sql_server.local.json` por defecto, o `CDLFORM_DATA_DIR` si se definio).
3. Archivo `config/sql_server.local.json` dentro del proyecto.

Para cada clave, las variables de entorno `CDLFORM_SQL_SERVER`, `CDLFORM_SQL_DATABASE`, `CDLFORM_SQL_USERNAME`, etc. tienen prioridad sobre el valor leido desde archivo.

Archivo esperado:

```json
{
  "server": "SERVIDOR_SQL",
  "database": "MetricsBetaProductivo",
  "username": "USUARIO_SQL",
  "password": "CLAVE_SQL",
  "driver": "ODBC Driver 18 for SQL Server",
  "encrypt": "no",
  "trust_server_certificate": "yes"
}
```

Acciones manuales:

- Confirmar con DBA la base objetivo. En este proyecto se ha mencionado `MetricsBetaProductivo`.
- Confirmar usuario SQL real de la app.
- Confirmar permisos sobre tablas usadas:
  - `[dbo].[formularios_operario]`
  - `[dbo].[preguntas]` y tablas relacionadas
  - `[dbo].[plantillas_preguntas]` y tablas relacionadas
  - `[dbo].[respuestas_formulario]`
  - `[dbo].[usuarios_gestion]`
  - `[dbo].[eventos_op_pendientes]`
  - `[dbo].[Apontamentos]`
  - `[dbo].[jbt_EstacaoXMaquinas]`
- Confirmar si el usuario puede ejecutar `CREATE TABLE` para `usuarios_gestion`; si no, pedir al DBA ejecutar `database/007_crear_usuarios_gestion.sql`.

Consulta util para confirmar identidad SQL:

```sql
USE [MetricsBetaProductivo];
GO

SELECT
    SUSER_SNAME() AS login_sql,
    USER_NAME() AS usuario_db,
    ORIGINAL_LOGIN() AS login_original;
GO
```

Si la app no ve usuarios de gestion, revisar primero que se esta mirando la misma base y el mismo usuario.

### 8.5 Configuracion de estacion Jobtrack

El archivo oficial de estacion es `C:\JOBTRACK\jobtrack.ini` en cada computador.

Ejemplo:

```ini
[JOBTRACK]
Estacao=ESTACION-76
idioma=1
```

Esta estacion se usa para resolver recursos/maquinas mediante SQL. El flujo automatico busca eventos pendientes solo para los `CodRecurso` asociados a esa estacion.

Regla actual del codigo:

1. si se instancia `JobtrackConfigService(ini_path=...)`, usa esa ruta explicita
2. si se define `CDLFORM_JOBTRACK_INI`, usa esa ruta
3. si no, usa `C:\JOBTRACK\jobtrack.ini`

`config/jobtrack.ini` queda solo como plantilla local/fallback operativo si se fuerza mediante `CDLFORM_JOBTRACK_INI`. No participa por defecto en el flujo actual.

Acciones manuales:

- Confirmar el codigo de estacion real del equipo.
- Confirmar que existe mapeo en `[dbo].[jbt_EstacaoXMaquinas]`.
- Confirmar que los recursos resultantes tienen eventos en `[dbo].[eventos_op_pendientes]` o apuntamientos en `[dbo].[Apontamentos]`.

Si la estacion esta mal:

- No se crean formularios.
- El modo automatico mostrara "No hay formularios pendientes".
- El worker devolvera JSON con `total_consultados` en cero o recursos vacios.

### 8.6 Scripts SQL manuales

Los scripts en `database/` no deberian ejecutarse impulsivamente en produccion. Se deben revisar y correr en orden solo si la base no tiene esas estructuras.

Orden conceptual:

1. `001_crear_tablas_formularios_operario.sql`
2. `001b_agregar_foreign_keys_formularios_operario_dba.sql`
3. `006_permitir_estado_en_progreso_formularios_operario.sql`
4. `007_crear_usuarios_gestion.sql`

Recomendacion:

- No ejecutar scripts historicos o de prueba que ya no esten en `database/`.
- Para la administracion de usuarios, si la tabla no existe o falta rol, ejecutar el `007`.
- Para estado `en_progreso`, ejecutar el `006` si SQL rechaza ese estado.

### 8.7 Usuarios de gestion

El usuario inicial puede provenir de fallback JSON/env, pero el objetivo es que quede en SQL.

Flujo recomendado:

1. DBA o administrador ejecuta `007_crear_usuarios_gestion.sql` en la DB correcta.
2. Iniciar la app con usuario fallback existente.
3. Entrar como admin.
4. Abrir administracion de usuarios.
5. Crear usuarios `admin` o `gestion`.
6. Desactivar o dejar solo como contingencia el fallback JSON.

Roles:

- `admin`: puede acceder a administracion de usuarios.
- `gestion`: puede usar dashboard/reportes/admin funcional, excepto administracion de usuarios si la UI lo restringe.

No crear rol supervisor. Supervisor viene desde Apontamentos y no corresponde a credenciales de esta aplicacion.

### 8.8 Accesos directos recomendados

Usar `.bat` estandar para no depender de que cada operador recuerde comandos.

Gestion:

```bat
C:\CDLform\run_gestion.bat
```

Operario automatico con UI:

```bat
C:\CDLform\run_operario.bat
```

Si hay varias versiones de Python instaladas, usar ruta absoluta:

```bat
C:\Users\<usuario>\AppData\Local\Programs\Python\Python314\python.exe C:\CDLform\main.py --modo normal
```

Para estaciones de operario, el estandar recomendado es iniciar `run_mqtt_listener.bat`. `run_operario.bat` se mantiene como respaldo/manual.

### 8.9 MQTT/watchdog: para que se usa

El flujo principal evita que cada estacion consulte SQL periodicamente. Un watchdog central consulta `eventos_op_pendientes`, publica avisos en Mosquitto y cada estacion reacciona ejecutando `main.py --modo auto`.

Importante:

- Mosquitto es solo transporte de avisos; SQL Server sigue siendo la fuente de verdad.
- `runtime\mqtt_sql_watchdog.py` corre en una maquina central con acceso SQL y al broker.
- `runtime\mqtt_station_listener.py` corre en cada estacion y debe iniciarse con `--initial-check --run-auto`.
- `run_operario.bat` queda como fallback manual o tarea programada lenta, por ejemplo cada 30 o 60 minutos.
- `worker_main.py` queda como herramienta tecnica o diagnostico.

Configuracion recomendada para listener por estacion:

| Campo | Valor sugerido |
| --- | --- |
| Name | `CDLform MQTT Listener` |
| Security options | Usuario Windows que usa la estacion y puede abrir UI |
| Run whether user is logged on or not | No recomendado si debe abrir UI visible |
| Trigger | At log on / al iniciar sesion del usuario |
| Action | Start a program |
| Program/script | `C:\CDLform\run_mqtt_listener.bat` |
| Add arguments | Vacio |
| Start in | `C:\CDLform` |

Configuracion recomendada para watchdog central:

| Campo | Valor sugerido |
| --- | --- |
| Name | `CDLform MQTT Watchdog` |
| Ubicacion | Maquina central/broker o servidor con acceso SQL |
| Action | Start a program |
| Program/script | `C:\CDLform\run_mqtt_watchdog.bat` |
| Start in | `C:\CDLform` |
| Config | `config\mqtt_watchdog.json` |

### 8.10 Task Scheduler como respaldo

Task Scheduler ya no debe ser el mecanismo principal de polling cada 5 minutos. Si se usa, debe ser una red de seguridad para recuperar pendientes ante caidas de MQTT, estaciones apagadas o reinicios.

Configuracion de respaldo sugerida:

| Campo | Valor sugerido |
| --- | --- |
| Name | `CDLform Operario Fallback` |
| Trigger | Daily, repetir cada 30 o 60 minutos |
| Program/script | `C:\CDLform\run_operario.bat` |
| Start in | `C:\CDLform` |
| Setting | `Do not start a new instance` |

Valores comunes de `Last Run Result`:

- `0x0`: ejecucion correcta.
- `0x1`: error generico del script o Python.
- `0x2`: ruta incorrecta o archivo no encontrado.
- `0x41301`: tarea en ejecucion.

### 8.11 Validar operario automatico manualmente antes de programarlo

En CMD o PowerShell:

```bat
cd /d C:\CDLform
python main.py --modo auto
```

Resultado esperado:

- Debe consultar la cola SQL de la estacion.
- Si hay formulario pendiente, debe abrir `FormularioOperarioView`.
- Si no hay pendientes, debe informar que no hay formularios disponibles.

La misma validacion se puede hacer con:

```bat
C:\CDLform\run_operario.bat
```

Si falla:

- Error de driver: revisar ODBC instalado.
- Error de login: revisar usuario/clave SQL.
- Error de permisos: pedir grant al DBA.
- Sin recursos: revisar `C:\JOBTRACK\jobtrack.ini` o `CDLFORM_JOBTRACK_INI`, y `jbt_EstacaoXMaquinas`.
- Sin plantilla: crear/activar plantilla para `CodSetor` + `CodRecurso`.

### 8.12 Validar modo automatico con UI

Comando:

```bat
cd /d C:\CDLform
python main.py --modo auto
```

Resultado esperado:

- Procesa cola o consulta.
- Si hay formulario pendiente, abre `FormularioOperarioView`.
- La pantalla ya debe mostrar operario desde apontamento.
- No debe aparecer selector manual de operario.

Si no abre formulario:

- Revisar mensaje informativo.
- Revisar `total_consultados`.
- Revisar si ya existe formulario completado para ese `IdApontamento`.
- Revisar si la cola marco el evento como procesado/error/omitido.
- Revisar plantilla activa para el contexto.

### 8.13 Respaldo de emergencia desde Apontamentos

La aplicacion conserva codigo de consulta directa a `[dbo].[Apontamentos]`, pero no esta conectado al worker ni al modo automatico. Su objetivo es servir como herramienta tecnica de recuperacion si la cola `[dbo].[eventos_op_pendientes]` queda inutilizable o si se necesita reconstruir formularios bajo supervision.

Ubicacion del codigo:

- `services/workflows/apontamento_procesado_service.py`
  - `sincronizar_y_crear_formularios_estacion_actual(...)`
  - `listar_apontamientos_pendientes_estacion_actual(...)`
- `services/jobtrack/apontamento_query_service.py`
  - `listar_apontamentos_estacion_actual(...)`
  - `listar_apontamentos_por_cod_recursos(...)`

Reglas de uso:

- No usarlo como tarea programada normal.
- No conectarlo nuevamente como fallback automatico sin una decision tecnica explicita.
- Ejecutarlo solo despues de revisar duplicados, estado de la cola y alcance por estacion/recurso.
- Guardar evidencia del resultado JSON si se usa para recuperacion.

Ejemplo tecnico para un desarrollador, ejecutado manualmente desde una consola controlada:

```bat
cd /d C:\CDLform
python -c "from services.workflows.apontamento_procesado_service import ApontamentoProcesadoService; import json; r=ApontamentoProcesadoService().sincronizar_y_crear_formularios_estacion_actual(limit_consulta=50, limit_creacion=50, solo_finalizados=True, solo_con_num_ordem=True); print(json.dumps(r, ensure_ascii=False, indent=2))"
```

Antes de usarlo:

1. Confirmar estacion en `C:\JOBTRACK\jobtrack.ini` o en la ruta definida por `CDLFORM_JOBTRACK_INI`.
2. Confirmar recursos asociados en `[dbo].[jbt_EstacaoXMaquinas]`.
3. Confirmar que la cola no esta funcionando o que la recuperacion se justifica.
4. Confirmar que existen plantillas activas para los contextos detectados.
5. Revisar que no se creen duplicados por `IdApontamento`.

### 8.14 Validar modo gestion

Comando:

```bat
cd /d C:\CDLform
python main.py --modo normal
```

Checklist:

- Login funciona con usuario SQL.
- Usuario admin ve administracion de usuarios.
- Usuario gestion no ve opciones de admin de usuarios.
- Dashboard carga sin demoras excesivas.
- Admin preguntas permite crear/editar en 4 fases.
- Reportes, acciones y auditoria cargan paginas de 100 registros.

### 8.15 Distribucion de nuevas versiones

Proceso recomendado para actualizar una estacion:

1. Cerrar aplicacion abierta.
2. Deshabilitar temporalmente tarea programada si se reemplazaran archivos.
3. Respaldar configuraciones locales:
   - `config/sql_server.local.json`
   - `C:\JOBTRACK\jobtrack.ini` o la ruta definida por `CDLFORM_JOBTRACK_INI`
   - JSON de login fallback si aun se usa.
4. Reemplazar carpeta de codigo o copiar nuevos archivos.
5. Restaurar/verificar configs locales.
6. Ejecutar scripts SQL nuevos si la version lo requiere.
7. Ejecutar:

```bat
python -m compileall -q .
```

8. Probar `main.py --modo normal`.
9. Probar `main.py --modo auto`.
10. Habilitar nuevamente listener MQTT/watchdog y, si aplica, Task Scheduler de fallback.

Si hay cambios de base de datos, coordinar ventana con DBA. No actualizar codigo que espera columnas nuevas antes de que la DB las tenga.

### 8.16 Configuracion minima por estacion

En una instalacion bien estandarizada, esto es lo unico que deberia revisarse por computador:

1. `C:\JOBTRACK\jobtrack.ini` o la ruta definida por `CDLFORM_JOBTRACK_INI`
2. usuario Windows que ejecuta la tarea
3. acceso a SQL/ODBC

Y esto deberia mantenerse igual para toda la planta:

1. estructura `C:\CDLform`
2. codigo fuente
3. dependencias Python
4. `run_mqtt_listener.bat` por estacion
5. `run_mqtt_watchdog.bat` en maquina central
6. `run_operario.bat` solo como fallback
7. nombre/frecuencia de la tarea de respaldo si se mantiene
### 8.17 Que queda pendiente para una distribucion mas robusta

Mejoras recomendadas:

- Estandarizar mejor el despliegue por estacion.
- Crear instalador o script de deploy cuando el flujo productivo ya este cerrado.
- Agregar logging formal al worker.
- Agregar verificacion de salud (`healthcheck`) para SQL/config/estacion.
- Llevar paginacion pesada a SQL.
- Reintroducir tests automatizados cuando el flujo se estabilice.

## 9. Prioridades para manana

Orden recomendado para retomar el trabajo:

1. Cerrar definicion del entorno operario para produccion:
   - estructura final de carpetas
   - comando exacto que correra en cada estacion
   - que archivos se editan por estacion
2. Dejar estandar de despliegue por estacion:
   - ruta final
   - nombre definitivo de la tarea programada
   - frecuencia
   - usuario de ejecucion
   - formato del log
3. Separar formalmente gestion vs operario:
   - gestion solo manual
   - operario con listener MQTT por estacion
   - watchdog MQTT central
   - Task Scheduler solo como fallback
   - `worker_main.py` solo como apoyo tecnico
4. Probar un caso real end-to-end con evento en cola:
   - detectar evento real
   - crear formulario
   - validar apertura en la estacion correcta
   - validar operario/supervisor
5. Armar carpeta release preliminar para estacion piloto.
6. Revisar pendientes de produccion:
   - permisos SQL
   - scripts SQL obligatorios
   - configuracion comun
   - configuracion por estacion

Checklist rapido para arrancar manana:

- [ ] Confirmar estructura final de `C:\CDLform`
- [ ] Confirmar si `sql_server.local.json` sera comun a todas las estaciones
- [ ] Confirmar que `jobtrack.ini` sera el unico archivo variable por estacion
- [ ] Definir nombre final de la tarea programada de operario
- [ ] Ejecutar prueba con evento real en cola
- [ ] Validar formulario abierto en la estacion correcta
- [ ] Preparar carpeta release para estacion piloto

## 10. Archivos eliminados recientemente

Estos archivos ya no pertenecen al flujo actual:

- `ui/seleccion_operario.py`
- `presenters/seleccion_operario_presenter.py`
- `services/forms/operario_service.py`
- `styles/seleccion_operario.qss`
- `models/operario.py`
- `core/result.py`
- `widgets/base_dialog.py`
- `assets/styles.qss`
- `test_auth_service.py`
- `test_formulario_operario.py`
- `test_formulario_service_plantilla.py`
- `test_sql.py`
- `test_sql_server_config.py`

Motivo principal: limpieza de referencias obsoletas, eliminacion de flujo manual de operario y retiro de tests para partir con documentacion tecnica.
