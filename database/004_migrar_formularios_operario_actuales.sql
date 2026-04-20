USE [MetricsBetaProductivo];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0001')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445456,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 03:54:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-10 09:56:53', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0001', 8064289445456, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 03:54:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-10 09:56:53', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0002')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445407,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 03:42:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = N'Se aplicaron las acciones correctivas.',
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-10 10:41:23', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0002', 8064289445407, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 03:42:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, N'Se aplicaron las acciones correctivas.',
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-10 10:41:23', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0003')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445405,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 02:22:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-10 11:15:44', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0003', 8064289445405, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 02:22:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-10 11:15:44', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0004')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445378,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 02:14:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-10 12:31:40', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0004', 8064289445378, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 02:14:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-10 12:31:40', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0005')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445376,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 01:30:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 17:27:52', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0005', 8064289445376, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 01:30:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-13 17:27:52', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0006')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445373,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 01:23:00',
        [operario_formulario] = N'Operario Prueba',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 17:30:27', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0006', 8064289445373, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 01:23:00',
        N'Operario Prueba', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-13 17:30:27', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0007')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445327,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-12',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-12 01:12:00',
        [operario_formulario] = N'10074125',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-20 14:40:33', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0007';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0007', 8064289445327, N'FLE05705', N'FLE05705',
        N'2026-02-12', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-12 01:12:00',
        N'10074125', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-20 14:40:33', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0008')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445319,
        [identificador] = N'FLE05705',
        [num_ordem] = N'FLE05705',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 23:48:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:11', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0008';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0008', 8064289445319, N'FLE05705', N'FLE05705',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 23:48:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:11', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0009')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445317,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 22:56:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:11', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:11', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0009', 8064289445317, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 22:56:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:11', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:11', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0010')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445316,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 22:00:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0010';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0010', 8064289445316, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 22:00:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0011')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445203,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 21:53:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0011';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0011', 8064289445203, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 21:53:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0012')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445113,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 18:56:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0012';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0012', 8064289445113, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 18:56:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0013')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445111,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 16:37:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = N'mmpp  golpeada',
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0013';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0013', 8064289445111, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 16:37:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, N'mmpp  golpeada',
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0014')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445088,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 16:29:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0014';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0014', 8064289445088, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 16:29:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0015')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445078,
        [identificador] = N'FLE38062',
        [num_ordem] = N'FLE38062',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 15:53:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0015';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0015', 8064289445078, N'FLE38062', N'FLE38062',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 15:53:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0016')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445076,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 2,
        [hora_fim] = N'2026-02-11 15:05:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0016';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0016', 8064289445076, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 2, N'2026-02-11 15:05:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0017')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445074,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 14:30:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0017';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0017', 8064289445074, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 14:30:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0018')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445062,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 13:30:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0018';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0018', 8064289445062, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 13:30:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0019')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445061,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 13:14:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0019';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0019', 8064289445061, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 13:14:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0020')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445059,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 12:50:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0020';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0020', 8064289445059, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 12:50:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0021')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445057,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 11:47:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0021';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0021', 8064289445057, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 11:47:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0022')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445055,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 11:45:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0022';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0022', 8064289445055, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 11:45:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0023')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445052,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 11:13:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0023';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0023', 8064289445052, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 11:13:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0024')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445050,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 11:10:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0024';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0024', 8064289445050, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 11:10:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0025')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445046,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 10:47:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:12', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0025';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0025', 8064289445046, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 10:47:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:12', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:12', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0026')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445045,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 10:44:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0026';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0026', 8064289445045, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 10:44:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0027')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445039,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 10:28:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0027';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0027', 8064289445039, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 10:28:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0028')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445035,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 10:20:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0028';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0028', 8064289445035, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 10:20:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0029')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445032,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 09:44:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0029';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0029', 8064289445032, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 09:44:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0030')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445030,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 09:42:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0030';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0030', 8064289445030, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 09:42:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0031')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445024,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 09:36:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0031';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0031', 8064289445024, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 09:36:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0032')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445019,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 09:26:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0032';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0032', 8064289445019, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 09:26:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0033')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445004,
        [identificador] = N'FLE37939',
        [num_ordem] = N'FLE37939',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 1,
        [hora_fim] = N'2026-02-11 09:13:00',
        [operario_formulario] = N'PMUNOZ',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0033';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0033', 8064289445004, N'FLE37939', N'FLE37939',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 1, N'2026-02-11 09:13:00',
        N'PMUNOZ', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0034')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230675,
        [identificador] = N'FLE38140',
        [num_ordem] = N'FLE38140',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 06:57:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0034';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0034', 8063221230675, N'FLE38140', N'FLE38140',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 06:57:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0035')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230651,
        [identificador] = N'FLE38140',
        [num_ordem] = N'FLE38140',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 06:46:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0035';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0035', 8063221230651, N'FLE38140', N'FLE38140',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 06:46:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0036')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230647,
        [identificador] = N'FLE38140',
        [num_ordem] = N'FLE38140',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 06:14:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0036';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0036', 8063221230647, N'FLE38140', N'FLE38140',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 06:14:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0037')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230644,
        [identificador] = N'FLE37679',
        [num_ordem] = N'FLE37679',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 06:12:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0037';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0037', 8063221230644, N'FLE37679', N'FLE37679',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 06:12:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0038')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230618,
        [identificador] = N'FLE37679',
        [num_ordem] = N'FLE37679',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 06:09:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0038';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0038', 8063221230618, N'FLE37679', N'FLE37679',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 06:09:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0039')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230614,
        [identificador] = N'FLE37679',
        [num_ordem] = N'FLE37679',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 05:36:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0039';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0039', 8063221230614, N'FLE37679', N'FLE37679',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 05:36:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0040')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230611,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 05:32:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:13', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0040';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0040', 8063221230611, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 05:32:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:13', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:13', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0041')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230585,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 05:26:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0041';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0041', 8063221230585, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 05:26:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0042')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230583,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 04:52:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0042';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0042', 8063221230583, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 04:52:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0043')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230581,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 04:48:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0043';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0043', 8063221230581, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 04:48:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0044')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230577,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 04:36:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0044';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0044', 8063221230577, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 04:36:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0045')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230566,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 04:30:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0045';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0045', 8063221230566, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 04:30:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0046')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8063221230564,
        [identificador] = N'FLE37403',
        [num_ordem] = N'FLE37403',
        [fecha_formulario] = N'2026-02-11',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-02-11 04:14:00',
        [operario_formulario] = N'13059605',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'pendiente_operario',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-07 15:22:14', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0046';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0046', 8063221230564, N'FLE37403', N'FLE37403',
        N'2026-02-11', N'UTECO', N'IMP_HUEGO', 3, N'2026-02-11 04:14:00',
        N'13059605', N'ESTACION-76', N'apontamento_sql', N'pendiente_operario',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-07 15:22:14', SYSDATETIME()), COALESCE(N'2026-04-07 15:22:14', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[formularios_operario] WHERE [id_formulario] = N'FORM-0047')
BEGIN
    UPDATE [dbo].[formularios_operario]
    SET
        [id_apontamento] = 8064289445460,
        [identificador] = N'FLE37847',
        [num_ordem] = N'FLE37847',
        [fecha_formulario] = N'2026-04-20',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [turno] = 3,
        [hora_fim] = N'2026-04-20 14:54:29.590000',
        [operario_formulario] = N'10074125',
        [estacion] = N'ESTACION-76',
        [evento_origen] = N'apontamento_sql',
        [estado] = N'completado',
        [descripcion_op] = NULL,
        [descripcion_proceso] = NULL,
        [observacion_general] = NULL,
        [id_plantilla_preguntas] = N'TPL-IMP_HUEGO-UTECO-V008',
        [version_plantilla_preguntas] = 8,
        [fecha_creacion] = COALESCE(N'2026-04-20 14:55:00', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-20 14:55:16', SYSDATETIME())
    WHERE [id_formulario] = N'FORM-0047';
END
ELSE
BEGIN
    INSERT INTO [dbo].[formularios_operario] (
        [id_formulario], [id_apontamento], [identificador], [num_ordem],
        [fecha_formulario], [cod_recurso], [cod_setor], [turno], [hora_fim],
        [operario_formulario], [estacion], [evento_origen], [estado],
        [descripcion_op], [descripcion_proceso], [observacion_general],
        [id_plantilla_preguntas], [version_plantilla_preguntas],
        [fecha_creacion], [fecha_actualizacion]
    )
    VALUES (
        N'FORM-0047', 8064289445460, N'FLE37847', N'FLE37847',
        N'2026-04-20', N'UTECO', N'IMP_HUEGO', 3, N'2026-04-20 14:54:29.590000',
        N'10074125', N'ESTACION-76', N'apontamento_sql', N'completado',
        NULL, NULL, NULL,
        N'TPL-IMP_HUEGO-UTECO-V008', 8,
        COALESCE(N'2026-04-20 14:55:00', SYSDATETIME()), COALESCE(N'2026-04-20 14:55:16', SYSDATETIME())
    );
END;

COMMIT TRANSACTION;
GO

SELECT
    COUNT(*) AS total_formularios
FROM [dbo].[formularios_operario];
GO

SELECT
    [estado],
    COUNT(*) AS total
FROM [dbo].[formularios_operario]
GROUP BY [estado]
ORDER BY [estado];
GO