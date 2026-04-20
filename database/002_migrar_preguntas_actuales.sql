USE [MetricsBetaProductivo];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0001',
        [texto] = N'¿Fueron retirados todos los residuos de la op anterior?',
        [tipo] = N'seleccion_unica',
        [obligatoria] = 1,
        [activa] = 0,
        [orden] = 1,
        [version] = 1,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 10:57:49', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 10:57:49', SYSDATETIME()),
        [fecha_desactivacion] = N'2026-04-13 10:57:49',
        [reemplazada_por] = N'PREG-0005'
    WHERE [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0001', N'PREG-0001', N'¿Fueron retirados todos los residuos de la op anterior?', N'seleccion_unica', 1, 0,
        1, 1, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 10:57:49', SYSDATETIME()),
        COALESCE(N'2026-04-13 10:57:49', SYSDATETIME()), N'2026-04-13 10:57:49', N'PREG-0005'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0001' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'Si',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0001'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0001', N'OPC-001', N'OPC-001', N'Si', NULL,
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0001' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'No',
        [accion_correctiva] = N'Deben ser retirados todos los restos una vez procesada la op',
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0001'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0001', N'OPC-002', N'OPC-002', N'No', N'Deben ser retirados todos los restos una vez procesada la op',
        1, 1, 2
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0002')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0002',
        [texto] = N'¿Fueron desechados todos los envases de...?',
        [tipo] = N'seleccion_multiple',
        [obligatoria] = 1,
        [activa] = 0,
        [orden] = 2,
        [version] = 1,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 10:50:30', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 10:50:30', SYSDATETIME()),
        [fecha_desactivacion] = N'2026-04-13 10:50:30',
        [reemplazada_por] = N'PREG-0003'
    WHERE [id_pregunta] = N'PREG-0002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0002', N'PREG-0002', N'¿Fueron desechados todos los envases de...?', N'seleccion_multiple', 1, 0,
        2, 1, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 10:50:30', SYSDATETIME()),
        COALESCE(N'2026-04-13 10:50:30', SYSDATETIME()), N'2026-04-13 10:50:30', N'PREG-0003'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0002' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'no todo lo de solvente',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0002'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0002', N'OPC-001', N'OPC-001', N'no todo lo de solvente', N'retirar lo restante',
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0002' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'todo lo de solvente',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0002'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0002', N'OPC-002', N'OPC-002', N'todo lo de solvente', NULL,
        1, 1, 2
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0002' AND [id_opcion] = N'OPC-003')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-003',
        [valor] = N'no todo lo de tinta',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 3,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0002'
      AND [id_opcion] = N'OPC-003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0002', N'OPC-003', N'OPC-003', N'no todo lo de tinta', N'retirar lo restante',
        1, 1, 3
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0002' AND [id_opcion] = N'OPC-004')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-004',
        [valor] = N'todo lo de tinta',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 4,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0002'
      AND [id_opcion] = N'OPC-004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0002', N'OPC-004', N'OPC-004', N'todo lo de tinta', NULL,
        1, 1, 4
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0002' AND [id_opcion] = N'OPC-005')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-005',
        [valor] = N'todo de todo',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 5,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0002'
      AND [id_opcion] = N'OPC-005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0002', N'OPC-005', N'OPC-005', N'todo de todo', NULL,
        1, 1, 5
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0003')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0002',
        [texto] = N'¿Fueron desechados todos los envases de...?',
        [tipo] = N'seleccion_multiple',
        [obligatoria] = 1,
        [activa] = 0,
        [orden] = 2,
        [version] = 2,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 10:50:30', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()),
        [fecha_desactivacion] = N'2026-04-13 15:21:20',
        [reemplazada_por] = N'PREG-0007'
    WHERE [id_pregunta] = N'PREG-0003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0003', N'PREG-0002', N'¿Fueron desechados todos los envases de...?', N'seleccion_multiple', 1, 0,
        2, 2, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 10:50:30', SYSDATETIME()),
        COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()), N'2026-04-13 15:21:20', N'PREG-0007'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0003' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'no todo lo de solvente',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0003'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0003', N'OPC-001', N'OPC-001', N'no todo lo de solvente', N'retirar lo restante',
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0003' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'todo lo de solvente',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0003'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0003', N'OPC-002', N'OPC-002', N'todo lo de solvente', NULL,
        1, 1, 2
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0003' AND [id_opcion] = N'OPC-003')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-003',
        [valor] = N'no todo lo de tinta',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 3,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0003'
      AND [id_opcion] = N'OPC-003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0003', N'OPC-003', N'OPC-003', N'no todo lo de tinta', N'retirar lo restante',
        1, 1, 3
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0003' AND [id_opcion] = N'OPC-004')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-004',
        [valor] = N'todo lo de tinta',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 4,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0003'
      AND [id_opcion] = N'OPC-004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0003', N'OPC-004', N'OPC-004', N'todo lo de tinta', NULL,
        1, 1, 4
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0003' AND [id_opcion] = N'OPC-005')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-005',
        [valor] = N'todo de todo',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 5,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0003'
      AND [id_opcion] = N'OPC-005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0003', N'OPC-005', N'OPC-005', N'todo de todo', NULL,
        1, 1, 5
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0002',
        [texto] = N'¿Fueron desechados todos los envases de...?',
        [tipo] = N'seleccion_multiple',
        [obligatoria] = 1,
        [activa] = 1,
        [orden] = 2,
        [version] = 3,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 10:53:06', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 10:53:06', SYSDATETIME()),
        [fecha_desactivacion] = NULL,
        [reemplazada_por] = NULL
    WHERE [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0004', N'PREG-0002', N'¿Fueron desechados todos los envases de...?', N'seleccion_multiple', 1, 1,
        2, 3, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 10:53:06', SYSDATETIME()),
        COALESCE(N'2026-04-13 10:53:06', SYSDATETIME()), NULL, NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0004' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'no todo lo de solvente',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0004'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0004', N'OPC-001', N'OPC-001', N'no todo lo de solvente', N'retirar lo restante',
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0004' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'todo lo de solvente',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0004'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0004', N'OPC-002', N'OPC-002', N'todo lo de solvente', NULL,
        1, 1, 2
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0004' AND [id_opcion] = N'OPC-003')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-003',
        [valor] = N'no todo lo de tinta',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 3,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0004'
      AND [id_opcion] = N'OPC-003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0004', N'OPC-003', N'OPC-003', N'no todo lo de tinta', N'retirar lo restante',
        1, 1, 3
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0004' AND [id_opcion] = N'OPC-004')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-004',
        [valor] = N'todo lo de tinta',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 4,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0004'
      AND [id_opcion] = N'OPC-004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0004', N'OPC-004', N'OPC-004', N'todo lo de tinta', NULL,
        1, 1, 4
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0004' AND [id_opcion] = N'OPC-005')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-005',
        [valor] = N'todo de todo',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 5,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0004'
      AND [id_opcion] = N'OPC-005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0004', N'OPC-005', N'OPC-005', N'todo de todo', NULL,
        1, 1, 5
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0005')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0001',
        [texto] = N'¿Fueron retirados todos los residuos de la op anterior?',
        [tipo] = N'seleccion_unica',
        [obligatoria] = 1,
        [activa] = 0,
        [orden] = 1,
        [version] = 2,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 10:57:49', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()),
        [fecha_desactivacion] = N'2026-04-13 11:06:20',
        [reemplazada_por] = N'PREG-0006'
    WHERE [id_pregunta] = N'PREG-0005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0005', N'PREG-0001', N'¿Fueron retirados todos los residuos de la op anterior?', N'seleccion_unica', 1, 0,
        1, 2, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 10:57:49', SYSDATETIME()),
        COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()), N'2026-04-13 11:06:20', N'PREG-0006'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0005' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'Si',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0005'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0005', N'OPC-001', N'OPC-001', N'Si', NULL,
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0005' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'No',
        [accion_correctiva] = N'Deben ser retirados todos los restos una vez procesada la op',
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0005'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0005', N'OPC-002', N'OPC-002', N'No', N'Deben ser retirados todos los restos una vez procesada la op',
        1, 1, 2
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0006')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0001',
        [texto] = N'¿Fueron retirados todos los residuos de la op anterior?',
        [tipo] = N'seleccion_unica',
        [obligatoria] = 1,
        [activa] = 1,
        [orden] = 1,
        [version] = 3,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 11:06:20', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()),
        [fecha_desactivacion] = NULL,
        [reemplazada_por] = NULL
    WHERE [id_pregunta] = N'PREG-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0006', N'PREG-0001', N'¿Fueron retirados todos los residuos de la op anterior?', N'seleccion_unica', 1, 1,
        1, 3, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()),
        COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()), NULL, NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0006' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'Si',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0006'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0006', N'OPC-001', N'OPC-001', N'Si', NULL,
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0006' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'No',
        [accion_correctiva] = N'Deben ser retirados todos los restos una vez procesada la op',
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0006'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0006', N'OPC-002', N'OPC-002', N'No', N'Deben ser retirados todos los restos una vez procesada la op',
        1, 1, 2
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0007')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0002',
        [texto] = N'¿Fueron desechados todos los envases de...?',
        [tipo] = N'seleccion_multiple',
        [obligatoria] = 1,
        [activa] = 0,
        [orden] = 2,
        [version] = 3,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}',
        [fecha_creacion] = COALESCE(N'2026-04-13 15:21:20', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()),
        [fecha_desactivacion] = NULL,
        [reemplazada_por] = NULL
    WHERE [id_pregunta] = N'PREG-0007';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0007', N'PREG-0002', N'¿Fueron desechados todos los envases de...?', N'seleccion_multiple', 1, 0,
        2, 3, N'{"cod_setor": ["IMP_HUEGO"], "cod_recurso": ["UTECO"], "turno": ["3"]}', COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()),
        COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()), NULL, NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0007' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'no todo lo de solvente',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0007'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0007', N'OPC-001', N'OPC-001', N'no todo lo de solvente', N'retirar lo restante',
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0007' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'todo lo de solvente',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0007'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0007', N'OPC-002', N'OPC-002', N'todo lo de solvente', NULL,
        1, 1, 2
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0007' AND [id_opcion] = N'OPC-003')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-003',
        [valor] = N'no todo lo de tinta',
        [accion_correctiva] = N'retirar lo restante',
        [activa] = 1,
        [version] = 1,
        [orden] = 3,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0007'
      AND [id_opcion] = N'OPC-003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0007', N'OPC-003', N'OPC-003', N'no todo lo de tinta', N'retirar lo restante',
        1, 1, 3
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0007' AND [id_opcion] = N'OPC-004')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-004',
        [valor] = N'todo lo de tinta',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 4,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0007'
      AND [id_opcion] = N'OPC-004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0007', N'OPC-004', N'OPC-004', N'todo lo de tinta', NULL,
        1, 1, 4
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0007' AND [id_opcion] = N'OPC-005')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-005',
        [valor] = N'todo de todo',
        [accion_correctiva] = NULL,
        [activa] = 1,
        [version] = 1,
        [orden] = 5,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0007'
      AND [id_opcion] = N'OPC-005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0007', N'OPC-005', N'OPC-005', N'todo de todo', NULL,
        1, 1, 5
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0008')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0008',
        [texto] = N'kbkj',
        [tipo] = N'seleccion_unica',
        [obligatoria] = 1,
        [activa] = 1,
        [orden] = 1,
        [version] = 1,
        [filtros_contexto_json] = N'{"cod_setor": ["IMP_FLEXO"]}',
        [fecha_creacion] = COALESCE(N'2026-04-15 16:10:58', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-15 16:10:58', SYSDATETIME()),
        [fecha_desactivacion] = NULL,
        [reemplazada_por] = NULL
    WHERE [id_pregunta] = N'PREG-0008';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0008', N'PREG-0008', N'kbkj', N'seleccion_unica', 1, 1,
        1, 1, N'{"cod_setor": ["IMP_FLEXO"]}', COALESCE(N'2026-04-15 16:10:58', SYSDATETIME()),
        COALESCE(N'2026-04-15 16:10:58', SYSDATETIME()), NULL, NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0008' AND [id_opcion] = N'OPC-001')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-001',
        [valor] = N'si',
        [accion_correctiva] = N'ijjk',
        [activa] = 1,
        [version] = 1,
        [orden] = 1,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0008'
      AND [id_opcion] = N'OPC-001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0008', N'OPC-001', N'OPC-001', N'si', N'ijjk',
        1, 1, 1
    );
END;
IF EXISTS (SELECT 1 FROM [dbo].[pregunta_opciones] WHERE [id_pregunta] = N'PREG-0008' AND [id_opcion] = N'OPC-002')
BEGIN
    UPDATE [dbo].[pregunta_opciones]
    SET
        [clave_opcion] = N'OPC-002',
        [valor] = N'no',
        [accion_correctiva] = N'jhvjv',
        [activa] = 1,
        [version] = 1,
        [orden] = 2,
        [fecha_actualizacion] = SYSDATETIME()
    WHERE [id_pregunta] = N'PREG-0008'
      AND [id_opcion] = N'OPC-002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[pregunta_opciones] (
        [id_pregunta], [id_opcion], [clave_opcion], [valor], [accion_correctiva],
        [activa], [version], [orden]
    )
    VALUES (
        N'PREG-0008', N'OPC-002', N'OPC-002', N'no', N'jhvjv',
        1, 1, 2
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[preguntas] WHERE [id_pregunta] = N'PREG-0009')
BEGIN
    UPDATE [dbo].[preguntas]
    SET
        [clave_pregunta] = N'PREG-0009',
        [texto] = N'hola',
        [tipo] = N'texto',
        [obligatoria] = 1,
        [activa] = 1,
        [orden] = 6,
        [version] = 1,
        [filtros_contexto_json] = N'{"cod_setor": ["EXTRUSION", "FOOD_SERVICE", "IMP_FLEXO"], "cod_recurso": ["UTECO"], "turno": ["1"]}',
        [fecha_creacion] = COALESCE(N'2026-04-17 10:16:09', [fecha_creacion]),
        [fecha_actualizacion] = COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()),
        [fecha_desactivacion] = NULL,
        [reemplazada_por] = NULL
    WHERE [id_pregunta] = N'PREG-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[preguntas] (
        [id_pregunta], [clave_pregunta], [texto], [tipo], [obligatoria], [activa],
        [orden], [version], [filtros_contexto_json], [fecha_creacion],
        [fecha_actualizacion], [fecha_desactivacion], [reemplazada_por]
    )
    VALUES (
        N'PREG-0009', N'PREG-0009', N'hola', N'texto', 1, 1,
        6, 1, N'{"cod_setor": ["EXTRUSION", "FOOD_SERVICE", "IMP_FLEXO"], "cod_recurso": ["UTECO"], "turno": ["1"]}', COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()),
        COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()), NULL, NULL
    );
END;


COMMIT TRANSACTION;
GO

SELECT
    (SELECT COUNT(*) FROM [dbo].[preguntas]) AS total_preguntas,
    (SELECT COUNT(*) FROM [dbo].[pregunta_opciones]) AS total_opciones;
GO