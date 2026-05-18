-- Configuracion de roles SQL recomendada para CDLform.
-- Ejecutar como DBA o usuario con permisos para crear roles y asignar permisos.
-- Los usuarios/login concretos pueden variar por ambiente.

IF DATABASE_PRINCIPAL_ID(N'cdlform_role_operario') IS NULL
    CREATE ROLE [cdlform_role_operario];

IF DATABASE_PRINCIPAL_ID(N'cdlform_role_gestion') IS NULL
    CREATE ROLE [cdlform_role_gestion];

IF DATABASE_PRINCIPAL_ID(N'cdlform_role_watchdog') IS NULL
    CREATE ROLE [cdlform_role_watchdog];

-- Watchdog: solo mira cola pendiente y resuelve estacion para publicar MQTT.
GRANT SELECT ON [dbo].[eventos_op_pendientes] TO [cdlform_role_watchdog];
GRANT SELECT ON [dbo].[jbt_EstacaoXMaquinas] TO [cdlform_role_watchdog];

-- Operario: consume cola de su estacion, crea/actualiza formularios y respuestas.
GRANT SELECT, UPDATE ON [dbo].[eventos_op_pendientes] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[Apontamentos] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[jbt_EstacaoXMaquinas] TO [cdlform_role_operario];
GRANT SELECT, INSERT, UPDATE ON [dbo].[formularios_operario] TO [cdlform_role_operario];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[respuestas_formulario] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[plantillas_preguntas] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[plantilla_preguntas_items] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[preguntas] TO [cdlform_role_operario];
GRANT SELECT ON [dbo].[pregunta_opciones] TO [cdlform_role_operario];

-- Gestion: administra catalogos, plantillas, usuarios y revisa formularios.
GRANT SELECT ON [dbo].[Apontamentos] TO [cdlform_role_gestion];
GRANT SELECT ON [dbo].[jbt_EstacaoXMaquinas] TO [cdlform_role_gestion];
GRANT SELECT ON [dbo].[eventos_op_pendientes] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[formularios_operario] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[respuestas_formulario] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[plantillas_preguntas] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[plantilla_preguntas_items] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[preguntas] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[pregunta_opciones] TO [cdlform_role_gestion];
GRANT SELECT, INSERT, UPDATE ON [dbo].[usuarios_gestion] TO [cdlform_role_gestion];

-- Asignacion ejemplo. Crear primero los usuarios en la base si no existen:
-- CREATE USER [cdlform_operario] FOR LOGIN [cdlform_operario];
-- CREATE USER [cdlform_gestion] FOR LOGIN [cdlform_gestion];
-- CREATE USER [cdlform_watchdog] FOR LOGIN [cdlform_watchdog];
-- ALTER ROLE [cdlform_role_operario] ADD MEMBER [cdlform_operario];
-- ALTER ROLE [cdlform_role_gestion] ADD MEMBER [cdlform_gestion];
-- ALTER ROLE [cdlform_role_watchdog] ADD MEMBER [cdlform_watchdog];
