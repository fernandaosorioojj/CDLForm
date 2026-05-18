-- Comentario CDLform: script SQL de instalacion/migracion; revisar antes de ejecutar en una base real.
-- No forma parte del flujo runtime diario de gestion, operario o MQTT.

USE [MetricsBetaProductivo];
GO

SET ANSI_NULLS ON;
GO

SET QUOTED_IDENTIFIER ON;
GO

IF OBJECT_ID(N'[dbo].[formularios_operario]', N'U') IS NOT NULL
BEGIN
    IF EXISTS (
        SELECT 1
        FROM sys.check_constraints
        WHERE [name] = N'CK_formularios_operario_estado'
          AND [parent_object_id] = OBJECT_ID(N'[dbo].[formularios_operario]')
    )
    BEGIN
        ALTER TABLE [dbo].[formularios_operario]
        DROP CONSTRAINT [CK_formularios_operario_estado];
    END;

    ALTER TABLE [dbo].[formularios_operario]
    ADD CONSTRAINT [CK_formularios_operario_estado] CHECK (
        [estado] IN (
            N'en_apertura',
            N'pendiente_operario',
            N'en_progreso',
            N'completado',
            N'cancelado',
            N'error'
        )
    );
END;
GO
