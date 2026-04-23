# Guia tecnica para desarrolladores CDLform

Ultima revision: 2026-04-23

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
- `repositories/`: persistencia SQL/JSON.
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

### 2.3 Worker programado

Entrada:

```text
worker_main.py
```

Secuencia:

```text
worker_main.py
  -> EventProcessor
  -> ApontamentoProcesadoService
  -> SQL
  -> imprime JSON de resultado
```

Uso esperado:

- Ideal para tarea programada de Windows Task Scheduler.
- Procesa/crea formularios, pero no abre UI.
- El modo UI automatico es el que abre formularios al operario.

Riesgos:

- Si el usuario Windows de la tarea no tiene permiso sobre la carpeta `data`, puede fallar configuracion, logs o acceso operativo aunque SQL este bien.
- El output JSON sirve para diagnostico; la tarea programada deberia guardar stdout/stderr si se quiere trazabilidad.

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
| `worker_main.py` | Entrada sin UI para tareas programadas. | Depende de SQL/configuracion del usuario que ejecuta la tarea. |

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
| `admin_login.example.json` | Ejemplo legacy de credenciales admin. | No usar como fuente real de produccion. |
| `admin_login.json` | Fallback legacy de login. | Puede ocultar falta de usuarios SQL. Revisar si se mantiene por continuidad. |
| `gestion_login.example.json` | Ejemplo actual de credenciales gestion. | No debe contener password plano. |
| `gestion_login.json` | Fallback actual de login. | Sensible; idealmente migrar a SQL y restringir acceso. |
| `jobtrack.ini` | Configuracion local de estacion Jobtrack. | Si estacion no existe o no mapea recursos, no se crean formularios. |
| `logging_config.py` | Configura logging rotativo. | Revisar permisos de escritura en directorio de logs. |
| `settings.py` | Define rutas, entorno, timezone y paths de configuracion. | Cambios aqui afectan app congelada, desarrollo y el estandar `data` del despliegue. |
| `sql_server.example.json` | Ejemplo de conexion SQL. | No poner credenciales reales. |
| `sql_server.local.json` | Configuracion local SQL. | Sensible; si apunta a DB equivocada, toda la app opera en otro ambiente. |
| `sql_server_config.py` | Construye connection string desde env/config. | Punto critico para errores ODBC, cifrado, permisos y ambiente. |
| `__init__.py` | Paquete Python. | Sin logica. |

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
| `002_migrar_preguntas_actuales.sql` | Migracion de preguntas. | Historico, pero relevante para reconstruir ambientes. |
| `003_migrar_plantillas_preguntas_actuales.sql` | Migracion de plantillas. | Necesario para entender versionado de plantillas. |
| `004_migrar_formularios_operario_actuales.sql` | Migracion de formularios. | Riesgo de duplicados si se reejecuta sin idempotencia. |
| `005_migrar_respuestas_formulario_actuales.sql` | Migracion de respuestas. | Alto riesgo: respuestas historicas y relaciones con preguntas. |
| `006_permitir_estado_en_progreso_formularios_operario.sql` | Permite estado `en_progreso`. | Si falta, la app usa compatibilidad parcial. Ejecutar con DBA si constraint falla. |
| `007_crear_usuarios_gestion.sql` | Crea/ajusta `usuarios_gestion`. | Debe ejecutarse en `MetricsBetaProductivo` u otra DB objetivo correcta. |

### `integrations`

| Archivo | Relevancia | Riesgos / notas |
| --- | --- | --- |
| `event_processor.py` | Fachada de procesamiento externo. Procesa exclusivamente la cola SQL productiva. | Si se reintroduce consulta directa a Apontamentos, debe quedar como emergencia controlada y no como fallback automatico. |
| `__init__.py` | Paquete Python. | Sin logica. |

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
| `base_repository.py` | Repositorio JSON generico usado como fallback/test/local. | No usar para produccion si se espera SQL. |
| `formulario_repository.py` | Persistencia de formularios en SQL o JSON. | Mapeo critico de columnas: operador/supervisor/plantilla/estado. |
| `plantilla_preguntas_repository.py` | Persistencia de plantillas/versiones. | Riesgo de activar multiples versiones si no se controla. |
| `pregunta_repository.py` | Persistencia de preguntas. | Opciones suelen serializarse; validar formato JSON. |
| `respuesta_repository.py` | Persistencia de respuestas. | Riesgo de duplicados si se guarda dos veces el mismo formulario. |
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
| `datetime_utils.py` | Utilidades de fecha/timezone. | Revisar formatos SQL vs ISO. |
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
- `data/sql_server.local.json`
- `config/sql_server.local.json` como respaldo de bootstrap/desarrollo
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

Esta seccion describe como deberia instalarse y operarse CDLform en una estacion o equipo de gestion. El proyecto hoy esta preparado como aplicacion Python/PyQt ejecutada desde carpeta, no como instalador formal. Si mas adelante se empaqueta con PyInstaller u otro instalador, las mismas responsabilidades se mantienen: binario/codigo, configuracion local, permisos SQL y tarea programada.

### 8.1 Conceptos clave

Hay tres formas practicas de ejecutar la aplicacion. En desarrollo se pueden usar scripts Python; para distribucion a estaciones se recomienda generar ejecutables `.exe`.

| Modo | Desarrollo | Distribucion EXE | Para que sirve |
| --- | --- | --- |
| Gestion | `python main.py --modo normal` | `CDLformGestion.exe` | Abre login, dashboard, administracion, reportes, auditoria y usuarios. |
| Operario automatico con UI | `python main.py --modo auto` | `CDLformOperario.exe` | Procesa eventos de cola y abre formulario al operario si existe pendiente. |
| Worker sin UI | `python worker_main.py` | `CDLformWorker.exe` | Corre en segundo plano o tarea programada para crear formularios sin abrir pantalla. |

La distribucion real puede usar los mismos scripts `.py` o accesos directos que ejecuten esos comandos. Lo importante es que el usuario Windows que los ejecute tenga:

- Python instalado o runtime empaquetado.
- Dependencias instaladas (`PyQt5`, `pyodbc`, etc.).
- Driver ODBC compatible.
- Acceso a SQL Server.
- Configuracion local correcta.
- Permisos de escritura en rutas de datos/logs.

### 8.2 Que se debe hacer manualmente

Antes de dejar el sistema operativo, hay pasos manuales que no conviene automatizar a ciegas:

1. Copiar o desplegar la carpeta de aplicacion en el equipo destino.
2. Confirmar que Python/dependencias o el ejecutable empaquetado funcionan.
3. Instalar/verificar driver ODBC de SQL Server.
4. Configurar conexion SQL del ambiente correcto.
5. Configurar estacion Jobtrack del equipo.
6. Ejecutar scripts SQL pendientes en la base correcta con DBA si aplica.
7. Crear o validar usuario administrador de gestion.
8. Crear accesos directos para gestion/operario si se usaran manualmente.
9. Crear tarea programada si el procesamiento debe correr solo.
10. Ejecutar checklist de validacion.

### 8.3 Estructura recomendada en el equipo destino

El estandar recomendado es separar ejecutables/codigo de una carpeta unica de datos.

Produccion:

```text
C:\CDLform\
  CDLformGestion\
    CDLformGestion.exe
    assets\
    config\
    docs\
    styles\
  CDLformOperario\
    CDLformOperario.exe
    assets\
    config\
    docs\
    styles\
  CDLformWorker\
    CDLformWorker.exe
    assets\
    config\
    docs\
    styles\
  data\
    jobtrack.ini
    sql_server.local.json
    gestion_login.json
    admin_login.json
    logs\
```

Desarrollo desde repo:

```text
C:\...\CDLform\
  config\
  docs\
  services\
  ...
  data\
```

Regla tecnica:

- En desarrollo, la app usa por defecto `.\data\`.
- En ejecutables congelados, la app usa por defecto `..\data\` respecto de cada `.exe`.
- Solo si se define `CDLFORM_DATA_DIR` se usa otra ruta.

Con esto evitamos depender de `%APPDATA%` y hacemos que ejecucion manual y Task Scheduler lean exactamente la misma configuracion.

### 8.4 Configuracion SQL

La conexion se arma en `config/sql_server_config.py` leyendo, en este orden:

1. Variable `CDLFORM_SQL_CONFIG_PATH`, si existe.
2. Archivo `data/sql_server.local.json`.
3. Archivo `config/sql_server.local.json` dentro del proyecto o del paquete, solo como respaldo de bootstrap/desarrollo.
4. Variables de entorno `CDLFORM_SQL_SERVER`, `CDLFORM_SQL_DATABASE`, etc.

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

El archivo oficial es `data/jobtrack.ini`. El archivo `config/jobtrack.ini` queda como respaldo de bootstrap/desarrollo.

Ejemplo:

```ini
[JOBTRACK]
Estacao=ESTACION-76
idioma=1
```

Esta estacion se usa para resolver recursos/maquinas mediante SQL. El flujo automatico busca eventos pendientes solo para los `CodRecurso` asociados a esa estacion.

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
3. `002_migrar_preguntas_actuales.sql`
4. `003_migrar_plantillas_preguntas_actuales.sql`
5. `004_migrar_formularios_operario_actuales.sql`
6. `005_migrar_respuestas_formulario_actuales.sql`
7. `006_permitir_estado_en_progreso_formularios_operario.sql`
8. `007_crear_usuarios_gestion.sql`

Recomendacion:

- En ambiente ya cargado, no repetir migraciones historicas sin revisar idempotencia.
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

Si se ejecuta desde codigo fuente, se pueden usar `.bat`:

Gestion:

```bat
cd /d C:\CDLform
python main.py --modo normal
```

Operario automatico con UI:

```bat
cd /d C:\CDLform
python main.py --modo auto
```

Worker sin UI:

```bat
cd /d C:\CDLform
python worker_main.py
```

Si hay varias versiones de Python instaladas, usar ruta absoluta:

```bat
C:\Users\<usuario>\AppData\Local\Programs\Python\Python314\python.exe C:\CDLform\main.py --modo normal
```

Para Task Scheduler es mejor configurar `Start in` en `C:\CDLform` y `Program/script` como `python.exe` o la ruta completa a Python.

Si se distribuye como EXE, los accesos directos deberian apuntar directamente a:

```text
C:\CDLform\CDLformGestion\CDLformGestion.exe
C:\CDLform\CDLformOperario\CDLformOperario.exe
```

El worker se usa desde Task Scheduler:

```text
C:\CDLform\CDLformWorker\CDLformWorker.exe
```

### 8.8.1 Generacion de ejecutables

El proyecto incluye preparacion de empaquetado en `packaging/`:

```text
packaging\entrypoints\gestion.py
packaging\entrypoints\operario.py
packaging\entrypoints\worker.py
packaging\build_exe.ps1
packaging\README.md
```

Instalar dependencias y PyInstaller en el equipo de build:

```bat
python -m pip install -r requirements.txt
```

Generar ejecutables:

```powershell
.\packaging\build_exe.ps1
```

Salida esperada:

```text
dist\exe\CDLformGestion\
dist\exe\CDLformOperario\
dist\exe\CDLformWorker\
```

Importante:

- No empaquetar credenciales reales dentro del exe.
- `data/sql_server.local.json` debe configurarse en destino.
- `data/jobtrack.ini` debe configurarse por estacion.
- El equipo destino aun necesita el driver ODBC de SQL Server.
- Si todas las estaciones usan la misma base/usuario SQL, `sql_server.local.json` puede ser igual para todas.
- `jobtrack.ini` normalmente cambia por estacion.

### 8.9 Task Scheduler: para que se usa

Task Scheduler deberia usarse para ejecutar el worker de forma periodica, por ejemplo cada 5 minutos. Su objetivo es mantener la cola procesada y crear formularios aunque nadie abra manualmente gestion.

Importante:

- El worker no abre pantalla.
- El worker procesa datos y crea formularios.
- La UI de operario se abre con `main.py --modo auto`, no con `worker_main.py`.

Configuracion recomendada:

| Campo | Valor sugerido |
| --- | --- |
| Name | `CDLform Worker Apontamentos` |
| Security options | Usuario Windows con permisos SQL/config local |
| Run whether user is logged on or not | Solo si no necesita UI y el entorno SQL funciona con ese usuario |
| Run with highest privileges | Activar si politicas locales lo requieren |
| Trigger | Daily, repetir cada 5 minutos indefinidamente |
| Action | Start a program |
| Program/script | `C:\CDLform\CDLformWorker\CDLformWorker.exe` |
| Add arguments | Vacio |
| Start in | `C:\CDLform\CDLformWorker` |

Ejemplo de Action:

```text
Program/script:
C:\CDLform\CDLformWorker\CDLformWorker.exe

Add arguments:
 

Start in:
C:\CDLform\CDLformWorker
```

Si se quiere guardar log de salida, Task Scheduler no maneja redireccion con comodidad en "Program/script" directo. En ese caso crear un `.bat` controlado, por ejemplo `run_worker.bat`:

```bat
@echo off
cd /d C:\CDLform\CDLformWorker
if not exist logs mkdir logs
CDLformWorker.exe >> logs\worker.log 2>&1
```

Luego en Task Scheduler:

```text
Program/script:
C:\CDLform\run_worker.bat

Start in:
C:\CDLform
```

Si se usa `.bat`, crear manualmente la carpeta `logs` o asegurar que el script pueda escribirla. En una version futura conviene agregar logging formal al worker.

### 8.10 Task Scheduler paso a paso

1. Abrir `Task Scheduler`.
2. Click en `Create Task...`.
3. Pestaña `General`:
   - Name: `CDLform Worker Apontamentos`.
   - Seleccionar usuario correcto.
   - Marcar `Run whether user is logged on or not` si correra sin sesion.
   - Marcar `Run with highest privileges` si corresponde.
4. Pestaña `Triggers`:
   - `New...`
   - Begin the task: `On a schedule`.
   - Settings: `Daily`.
   - Advanced settings: `Repeat task every: 5 minutes`.
   - For a duration of: `Indefinitely`.
   - Enabled: marcado.
5. Pestaña `Actions`:
   - `New...`
   - Action: `Start a program`.
   - Program/script: `C:\CDLform\CDLformWorker\CDLformWorker.exe` o `C:\CDLform\run_worker.bat`.
   - Add arguments: vacio si se usa EXE.
   - Start in: `C:\CDLform\CDLformWorker`.
6. Pestaña `Conditions`:
   - Desmarcar opciones de energia que impidan correr si no aplica.
7. Pestaña `Settings`:
   - Permitir ejecucion bajo demanda.
   - Si ya esta corriendo: elegir `Do not start a new instance` para evitar procesos duplicados.
8. Guardar.
9. Click derecho sobre la tarea -> `Run`.
10. Revisar `Last Run Result`.

Valores comunes de `Last Run Result`:

- `0x0`: ejecucion correcta.
- `0x1`: error generico del script o Python.
- `0x2`: ruta incorrecta o archivo no encontrado.
- `0x41301`: tarea en ejecucion.

### 8.11 Validar worker manualmente antes de programarlo

En CMD o PowerShell:

```bat
cd /d C:\CDLform
python worker_main.py
```

Con EXE:

```bat
cd /d C:\CDLform\CDLformWorker
CDLformWorker.exe
```

Resultado esperado:

- Debe imprimir JSON.
- `origen_sincronizacion` debe indicar `cola_sql`.
- `total_consultados` muestra cuantos eventos de cola reviso.
- `total_formularios_creados` indica cuantos formularios nuevos se crearon.
- `errores` deberia venir vacio o con mensajes claros.

Si falla:

- Error de driver: revisar ODBC instalado.
- Error de login: revisar usuario/clave SQL.
- Error de permisos: pedir grant al DBA.
- Sin recursos: revisar `jobtrack.ini` y `jbt_EstacaoXMaquinas`.
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

1. Confirmar estacion en `data/jobtrack.ini`.
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
   - `data/sql_server.local.json`
   - `data/jobtrack.ini`
   - JSON de login fallback si aun se usa en `data/`.
4. Reemplazar carpeta de codigo o copiar nuevos archivos.
5. Restaurar/verificar configs locales.
6. Ejecutar scripts SQL nuevos si la version lo requiere.
7. Ejecutar:

```bat
python -m compileall -q .
```

8. Probar `main.py --modo normal`.
9. Probar `worker_main.py` o `CDLformWorker.exe`, segun formato desplegado.
10. Habilitar nuevamente Task Scheduler.

Si hay cambios de base de datos, coordinar ventana con DBA. No actualizar codigo que espera columnas nuevas antes de que la DB las tenga.

### 8.16 Que queda pendiente para una distribucion mas robusta

Mejoras recomendadas:

- Empaquetar con PyInstaller para no depender de Python instalado en cada equipo.
- Crear instalador o script de deploy.
- Separar configs sensibles fuera de la carpeta versionada.
- Agregar logging formal al worker.
- Agregar verificacion de salud (`healthcheck`) para SQL/config/estacion.
- Llevar paginacion pesada a SQL.
- Reintroducir tests automatizados cuando el flujo se estabilice.

### 8.17 Estandar manual por estacion

La instalacion manual de cada estacion deberia seguir siempre la misma secuencia:

1. Copiar la release a `C:\CDLform\`.
2. Verificar que exista `C:\CDLform\data\`.
3. Crear o ajustar `C:\CDLform\data\sql_server.local.json`.
4. Crear o ajustar `C:\CDLform\data\jobtrack.ini`.
5. Confirmar permisos de lectura/escritura sobre `C:\CDLform\data\logs\`.
6. Probar manualmente `CDLformWorker.exe`.
7. Revisar el JSON de salida o el log.
8. Recien despues crear la tarea programada.

Regla operativa:

- `sql_server.local.json`: normalmente comun a todas las estaciones si usan el mismo ambiente SQL.
- `jobtrack.ini`: normalmente cambia por estacion.
- `logs\`: siempre local a la maquina.

Esto deja un solo lugar oficial para mirar configuracion cuando haya que diagnosticar.

## 9. Prioridades para manana

Orden recomendado para retomar el trabajo:

1. Cerrar definicion del entorno operario para produccion:
   - estructura final de carpetas
   - contenido de `CDLformWorker.exe`
   - contenido de `CDLformOperario.exe`
   - que archivos se editan por estacion
2. Dejar estandar de despliegue por estacion:
   - ruta final
   - nombre definitivo de la tarea programada
   - frecuencia
   - usuario de ejecucion
   - formato del log
3. Separar formalmente gestion vs operario:
   - gestion solo manual con `CDLformGestion.exe`
   - operario con worker programado
   - operario con UI local solo cuando corresponda
4. Probar un caso real end-to-end con evento en cola:
   - detectar evento real
   - crear formulario
   - validar apertura en la estacion correcta
   - validar operario/supervisor
5. Armar paquete release preliminar para estacion piloto.
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
