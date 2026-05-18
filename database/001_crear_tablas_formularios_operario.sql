-- Comentario CDLform: script SQL de instalacion/migracion; revisar antes de ejecutar en una base real.
-- No forma parte del flujo runtime diario de gestion, operario o MQTT.

USE [MetricsBetaProductivo];
GO

SET ANSI_NULLS ON;
GO

SET QUOTED_IDENTIFIER ON;
GO

IF OBJECT_ID(N'[dbo].[preguntas]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[preguntas] (
        [id_pregunta]            NVARCHAR(50)   NOT NULL,
        [clave_pregunta]         NVARCHAR(50)   NOT NULL,
        [texto]                  NVARCHAR(1000) NOT NULL,
        [tipo]                   NVARCHAR(50)   NOT NULL,
        [obligatoria]            BIT            NOT NULL CONSTRAINT [DF_preguntas_obligatoria] DEFAULT (1),
        [activa]                 BIT            NOT NULL CONSTRAINT [DF_preguntas_activa] DEFAULT (1),
        [orden]                  INT            NOT NULL CONSTRAINT [DF_preguntas_orden] DEFAULT (1),
        [version]                INT            NOT NULL CONSTRAINT [DF_preguntas_version] DEFAULT (1),
        [filtros_contexto_json]  NVARCHAR(MAX)  NULL,
        [fecha_creacion]         DATETIME2(0)   NOT NULL CONSTRAINT [DF_preguntas_fecha_creacion] DEFAULT (SYSDATETIME()),
        [fecha_actualizacion]    DATETIME2(0)   NOT NULL CONSTRAINT [DF_preguntas_fecha_actualizacion] DEFAULT (SYSDATETIME()),
        [fecha_desactivacion]    DATETIME2(0)   NULL,
        [reemplazada_por]        NVARCHAR(50)   NULL,
        CONSTRAINT [PK_preguntas] PRIMARY KEY CLUSTERED ([id_pregunta]),
        CONSTRAINT [CK_preguntas_tipo] CHECK (
            [tipo] IN (
                N'texto',
                N'numero',
                N'si_no',
                N'seleccion_unica',
                N'seleccion_multiple'
            )
        ),
        CONSTRAINT [CK_preguntas_version] CHECK ([version] > 0),
        CONSTRAINT [CK_preguntas_orden] CHECK ([orden] > 0)
    );
END;
GO

IF OBJECT_ID(N'[dbo].[pregunta_opciones]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[pregunta_opciones] (
        [id_pregunta]          NVARCHAR(50)   NOT NULL,
        [id_opcion]            NVARCHAR(50)   NOT NULL,
        [clave_opcion]         NVARCHAR(50)   NOT NULL,
        [valor]                NVARCHAR(500)  NOT NULL,
        [accion_correctiva]    NVARCHAR(1000) NULL,
        [activa]               BIT            NOT NULL CONSTRAINT [DF_pregunta_opciones_activa] DEFAULT (1),
        [version]              INT            NOT NULL CONSTRAINT [DF_pregunta_opciones_version] DEFAULT (1),
        [orden]                INT            NOT NULL CONSTRAINT [DF_pregunta_opciones_orden] DEFAULT (1),
        [fecha_creacion]       DATETIME2(0)   NOT NULL CONSTRAINT [DF_pregunta_opciones_fecha_creacion] DEFAULT (SYSDATETIME()),
        [fecha_actualizacion]  DATETIME2(0)   NOT NULL CONSTRAINT [DF_pregunta_opciones_fecha_actualizacion] DEFAULT (SYSDATETIME()),
        CONSTRAINT [PK_pregunta_opciones] PRIMARY KEY CLUSTERED ([id_pregunta], [id_opcion]),
        CONSTRAINT [CK_pregunta_opciones_version] CHECK ([version] > 0),
        CONSTRAINT [CK_pregunta_opciones_orden] CHECK ([orden] > 0)
    );
END;
GO

IF OBJECT_ID(N'[dbo].[plantillas_preguntas]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[plantillas_preguntas] (
        [id_plantilla]         NVARCHAR(100) NOT NULL,
        [clave_plantilla]      NVARCHAR(100) NOT NULL,
        [cod_recurso]          NVARCHAR(100) NOT NULL,
        [cod_setor]            NVARCHAR(100) NOT NULL,
        [version]              INT           NOT NULL,
        [activa]               BIT           NOT NULL CONSTRAINT [DF_plantillas_preguntas_activa] DEFAULT (1),
        [fecha_creacion]       DATETIME2(0)  NOT NULL CONSTRAINT [DF_plantillas_preguntas_fecha_creacion] DEFAULT (SYSDATETIME()),
        [fecha_desactivacion]  DATETIME2(0)  NULL,
        CONSTRAINT [PK_plantillas_preguntas] PRIMARY KEY CLUSTERED ([id_plantilla]),
        CONSTRAINT [CK_plantillas_preguntas_version] CHECK ([version] > 0)
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'UX_plantillas_preguntas_clave_version'
      AND [object_id] = OBJECT_ID(N'[dbo].[plantillas_preguntas]')
)
AND OBJECT_ID(N'[dbo].[plantillas_preguntas]', N'U') IS NOT NULL
BEGIN
    CREATE UNIQUE INDEX [UX_plantillas_preguntas_clave_version]
    ON [dbo].[plantillas_preguntas] ([clave_plantilla], [version]);
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'UX_plantillas_preguntas_activa_contexto'
      AND [object_id] = OBJECT_ID(N'[dbo].[plantillas_preguntas]')
)
AND OBJECT_ID(N'[dbo].[plantillas_preguntas]', N'U') IS NOT NULL
BEGIN
    CREATE UNIQUE INDEX [UX_plantillas_preguntas_activa_contexto]
    ON [dbo].[plantillas_preguntas] ([cod_setor], [cod_recurso])
    WHERE [activa] = 1;
END;
GO

IF OBJECT_ID(N'[dbo].[plantilla_preguntas_items]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[plantilla_preguntas_items] (
        [id_plantilla]  NVARCHAR(100) NOT NULL,
        [id_pregunta]   NVARCHAR(50)  NOT NULL,
        [orden]         INT           NOT NULL,
        CONSTRAINT [PK_plantilla_preguntas_items] PRIMARY KEY CLUSTERED ([id_plantilla], [id_pregunta]),
        CONSTRAINT [CK_plantilla_preguntas_items_orden] CHECK ([orden] > 0)
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'UX_plantilla_preguntas_items_orden'
      AND [object_id] = OBJECT_ID(N'[dbo].[plantilla_preguntas_items]')
)
AND OBJECT_ID(N'[dbo].[plantilla_preguntas_items]', N'U') IS NOT NULL
BEGIN
    CREATE UNIQUE INDEX [UX_plantilla_preguntas_items_orden]
    ON [dbo].[plantilla_preguntas_items] ([id_plantilla], [orden]);
END;
GO

IF OBJECT_ID(N'[dbo].[formularios_operario]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[formularios_operario] (
        [id_formulario]                  NVARCHAR(50)   NOT NULL,
        [id_evento_cola]                 BIGINT         NULL,
        [id_apontamento]                 BIGINT         NOT NULL,
        [identificador]                  NVARCHAR(100)  NOT NULL,
        [num_ordem]                      NVARCHAR(50)   NULL,
        [fecha_formulario]               DATE           NOT NULL,
        [cod_recurso]                    NVARCHAR(100)  NOT NULL,
        [cod_setor]                      NVARCHAR(100)  NOT NULL,
        [turno]                          INT            NULL,
        [hora_inicio]                    DATETIME2(3)   NULL,
        [hora_fim]                       DATETIME2(3)   NULL,
        [operador_apontamento]           NVARCHAR(100)  NULL,
        [supervisor_apontamento]         NVARCHAR(100)  NULL,
        [operario_formulario]            NVARCHAR(100)  NULL,
        [estacion]                       NVARCHAR(100)  NULL,
        [estado]                         NVARCHAR(50)   NOT NULL CONSTRAINT [DF_formularios_operario_estado] DEFAULT (N'en_apertura'),
        [evento_origen]                  NVARCHAR(50)   NOT NULL CONSTRAINT [DF_formularios_operario_evento_origen] DEFAULT (N'cola_sql'),
        [descripcion_op]                 NVARCHAR(1000) NULL,
        [descripcion_proceso]            NVARCHAR(1000) NULL,
        [observacion_general]            NVARCHAR(2000) NULL,
        [id_plantilla_preguntas]         NVARCHAR(100)  NOT NULL,
        [version_plantilla_preguntas]    INT            NOT NULL,
        [fecha_creacion]                 DATETIME2(0)   NOT NULL CONSTRAINT [DF_formularios_operario_fecha_creacion] DEFAULT (SYSDATETIME()),
        [fecha_actualizacion]            DATETIME2(0)   NOT NULL CONSTRAINT [DF_formularios_operario_fecha_actualizacion] DEFAULT (SYSDATETIME()),
        CONSTRAINT [PK_formularios_operario] PRIMARY KEY CLUSTERED ([id_formulario]),
        CONSTRAINT [CK_formularios_operario_estado] CHECK (
            [estado] IN (
                N'en_apertura',
                N'pendiente_operario',
                N'en_progreso',
                N'completado',
                N'cancelado',
                N'error'
            )
        ),
        CONSTRAINT [CK_formularios_operario_version_plantilla] CHECK ([version_plantilla_preguntas] > 0)
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'UX_formularios_operario_id_apontamento'
      AND [object_id] = OBJECT_ID(N'[dbo].[formularios_operario]')
)
AND OBJECT_ID(N'[dbo].[formularios_operario]', N'U') IS NOT NULL
BEGIN
    CREATE UNIQUE INDEX [UX_formularios_operario_id_apontamento]
    ON [dbo].[formularios_operario] ([id_apontamento]);
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'IX_formularios_operario_estado_fecha'
      AND [object_id] = OBJECT_ID(N'[dbo].[formularios_operario]')
)
AND OBJECT_ID(N'[dbo].[formularios_operario]', N'U') IS NOT NULL
BEGIN
    CREATE INDEX [IX_formularios_operario_estado_fecha]
    ON [dbo].[formularios_operario] ([estado], [fecha_formulario] DESC);
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'IX_formularios_operario_contexto'
      AND [object_id] = OBJECT_ID(N'[dbo].[formularios_operario]')
)
AND OBJECT_ID(N'[dbo].[formularios_operario]', N'U') IS NOT NULL
BEGIN
    CREATE INDEX [IX_formularios_operario_contexto]
    ON [dbo].[formularios_operario] ([cod_setor], [cod_recurso], [fecha_formulario] DESC);
END;
GO

IF OBJECT_ID(N'[dbo].[respuestas_formulario]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[respuestas_formulario] (
        [id_respuesta]                  NVARCHAR(50)   NOT NULL,
        [id_formulario]                 NVARCHAR(50)   NOT NULL,
        [id_pregunta]                   NVARCHAR(50)   NOT NULL,
        [id_opcion]                     NVARCHAR(50)   NULL,
        [respuesta_texto]               NVARCHAR(2000) NULL,
        [respuesta_numero]              DECIMAL(18, 4) NULL,
        [accion_correctiva_aplicada]    NVARCHAR(1000) NULL,
        [fecha_creacion]                DATETIME2(0)   NOT NULL CONSTRAINT [DF_respuestas_formulario_fecha_creacion] DEFAULT (SYSDATETIME()),
        CONSTRAINT [PK_respuestas_formulario] PRIMARY KEY CLUSTERED ([id_respuesta]),
        CONSTRAINT [CK_respuestas_formulario_contenido] CHECK (
            [respuesta_texto] IS NOT NULL
            OR [respuesta_numero] IS NOT NULL
            OR [id_opcion] IS NOT NULL
        )
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'IX_respuestas_formulario_id_formulario'
      AND [object_id] = OBJECT_ID(N'[dbo].[respuestas_formulario]')
)
AND OBJECT_ID(N'[dbo].[respuestas_formulario]', N'U') IS NOT NULL
BEGIN
    CREATE INDEX [IX_respuestas_formulario_id_formulario]
    ON [dbo].[respuestas_formulario] ([id_formulario]);
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE [name] = N'IX_respuestas_formulario_accion_correctiva'
      AND [object_id] = OBJECT_ID(N'[dbo].[respuestas_formulario]')
)
AND OBJECT_ID(N'[dbo].[respuestas_formulario]', N'U') IS NOT NULL
BEGIN
    CREATE INDEX [IX_respuestas_formulario_accion_correctiva]
    ON [dbo].[respuestas_formulario] ([fecha_creacion] DESC)
    WHERE [accion_correctiva_aplicada] IS NOT NULL;
END;
GO
