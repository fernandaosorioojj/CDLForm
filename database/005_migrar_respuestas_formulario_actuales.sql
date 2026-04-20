USE [MetricsBetaProductivo];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

-- Respuestas validas a migrar: 66
-- Respuestas omitidas por id_formulario/id_pregunta invalido: 3

-- OMITIDA RESP-0049: id_formulario=FORM-0001; id_pregunta=[{'ID_PREGUNTA': 'PREG-0001', 'TEXTO': '¿LA MÁQUINA QUEDÓ LIMPIA AL CIERRE DE LA OP?', 'TIPO': 'SELECCION_UNICA', 'ACTIVA': TRUE, 'OBLIGATORIA': TRUE, 'ORDEN': 1, 'FILTROS_CONTEXTO': {'COD_SETOR': ['S
-- OMITIDA RESP-0050: id_formulario=FORM-0001; id_pregunta=[{'ID_PREGUNTA': 'PREG-0001', 'TEXTO': '¿LA MÁQUINA QUEDÓ LIMPIA AL CIERRE DE LA OP?', 'TIPO': 'SELECCION_UNICA', 'ACTIVA': TRUE, 'OBLIGATORIA': TRUE, 'ORDEN': 1, 'FILTROS_CONTEXTO': {'COD_SETOR': ['S
-- OMITIDA RESP-0051: id_formulario=FORM-0001; id_pregunta=[{'ID_PREGUNTA': 'PREG-0001', 'TEXTO': '¿LA MÁQUINA QUEDÓ LIMPIA AL CIERRE DE LA OP?', 'TIPO': 'SELECCION_UNICA', 'ACTIVA': TRUE, 'OBLIGATORIA': TRUE, 'ORDEN': 1, 'FILTROS_CONTEXTO': {'COD_SETOR': ['S

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0001')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = N'Revisar control final antes de cerrar.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0001', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-002', N'Revisar control final antes de cerrar.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0002')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 1250.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0002', N'FORM-0001', N'PREG-0002', NULL,
        1250.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0003')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'Turno sin incidentes mayores.',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0003', N'FORM-0001', N'PREG-0003', N'Turno sin incidentes mayores.',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0004')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0004', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0005')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 66.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0005', N'FORM-0001', N'PREG-0002', NULL,
        66.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0006')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'ninguna',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0006', N'FORM-0001', N'PREG-0003', N'ninguna',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0007')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0002',
        [accion_correctiva_aplicada] = N'Realizar limpieza y registrar novedad.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0007';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0007', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-0002', N'Realizar limpieza y registrar novedad.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0008')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 0.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0008';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0008', N'FORM-0001', N'PREG-0002', NULL,
        0.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0009')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0002',
        [accion_correctiva_aplicada] = N'Realizar limpieza y registrar novedad.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0009', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-0002', N'Realizar limpieza y registrar novedad.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0010')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 1.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0010';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0010', N'FORM-0001', N'PREG-0002', NULL,
        1.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0011')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0002',
        [accion_correctiva_aplicada] = N'Realizar limpieza y registrar novedad.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0011';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0011', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-0002', N'Realizar limpieza y registrar novedad.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0012')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 1.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0012';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0012', N'FORM-0001', N'PREG-0002', NULL,
        1.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0013')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'Nada',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0013';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0013', N'FORM-0001', N'PREG-0003', N'Nada',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0014')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0014';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0014', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0015')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 10.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0015';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0015', N'FORM-0001', N'PREG-0002', NULL,
        10.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0016')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'NO',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0016';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0016', N'FORM-0001', N'PREG-0003', N'NO',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0017')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0017';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0017', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0018')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 1.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0018';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0018', N'FORM-0001', N'PREG-0002', NULL,
        1.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0019')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0019';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0019', N'FORM-0001', N'PREG-0003', N'No',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0020')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0020';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0020', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0021')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 2.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0021';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0021', N'FORM-0001', N'PREG-0002', NULL,
        2.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0022')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N's',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0022';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0022', N'FORM-0001', N'PREG-0003', N's',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0023')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0023';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0023', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0024')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 9.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0024';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0024', N'FORM-0001', N'PREG-0002', NULL,
        9.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0025')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0025';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0025', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0026')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 9.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0026';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0026', N'FORM-0001', N'PREG-0002', NULL,
        9.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0027')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'.',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0027';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0027', N'FORM-0001', N'PREG-0003', N'.',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0028')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0028';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0028', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0029')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 2.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0029';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0029', N'FORM-0001', N'PREG-0002', NULL,
        2.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0030')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'no',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0030';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0030', N'FORM-0001', N'PREG-0003', N'no',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0031')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0031';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0031', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0032')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 3.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0032';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0032', N'FORM-0001', N'PREG-0002', NULL,
        3.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0033')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N's',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0033';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0033', N'FORM-0001', N'PREG-0003', N's',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0034')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0034';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0034', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0035')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 34.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0035';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0035', N'FORM-0001', N'PREG-0002', NULL,
        34.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0036')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'Nada',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0036';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0036', N'FORM-0001', N'PREG-0003', N'Nada',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0037')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0037';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0037', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0038')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 9.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0038';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0038', N'FORM-0001', N'PREG-0002', NULL,
        9.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0039')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'.',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0039';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0039', N'FORM-0001', N'PREG-0003', N'.',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0040')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0002',
        [accion_correctiva_aplicada] = N'Realizar limpieza y registrar novedad.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0040';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0040', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-0002', N'Realizar limpieza y registrar novedad.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0041')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 2.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0041';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0041', N'FORM-0001', N'PREG-0002', NULL,
        2.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0042')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N's',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0042';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0042', N'FORM-0001', N'PREG-0003', N's',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0043')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0002',
        [accion_correctiva_aplicada] = N'Realizar limpieza y registrar novedad.',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0043';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0043', N'FORM-0001', N'PREG-0001', N'No',
        NULL, N'OPC-0002', N'Realizar limpieza y registrar novedad.', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0044')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 90.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0044';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0044', N'FORM-0001', N'PREG-0002', NULL,
        90.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0045')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N'reproceso',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0045';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0045', N'FORM-0001', N'PREG-0003', N'reproceso',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0046')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Sí',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-0001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0046';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0046', N'FORM-0001', N'PREG-0001', N'Sí',
        NULL, N'OPC-0001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0047')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = NULL,
        [respuesta_numero] = 3.0,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0047';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0047', N'FORM-0001', N'PREG-0002', NULL,
        3.0, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0048')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0001',
        [id_pregunta] = N'PREG-0003',
        [respuesta_texto] = N's',
        [respuesta_numero] = NULL,
        [id_opcion] = NULL,
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0048';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0048', N'FORM-0001', N'PREG-0003', N's',
        NULL, NULL, NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0052')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0002',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'Si',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0052';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0052', N'FORM-0002', N'PREG-0001', N'Si',
        NULL, N'OPC-001', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0053')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0002',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'no todo lo de solvente',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0053';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0053', N'FORM-0002', N'PREG-0002', N'no todo lo de solvente',
        NULL, N'OPC-001', N'retirar lo restante', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0054')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0002',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'no todo lo de tinta',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-003',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0054';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0054', N'FORM-0002', N'PREG-0002', N'no todo lo de tinta',
        NULL, N'OPC-003', N'retirar lo restante', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0055')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0003',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = N'Deben ser retirados todos los restos una vez procesada la op',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0055';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0055', N'FORM-0003', N'PREG-0001', N'No',
        NULL, N'OPC-002', N'Deben ser retirados todos los restos una vez procesada la op', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0056')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0003',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'todo lo de solvente',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0056';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0056', N'FORM-0003', N'PREG-0002', N'todo lo de solvente',
        NULL, N'OPC-002', NULL, COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0057')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0003',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'no todo lo de tinta',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-003',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0057';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0057', N'FORM-0003', N'PREG-0002', N'no todo lo de tinta',
        NULL, N'OPC-003', N'retirar lo restante', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0058')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0004',
        [id_pregunta] = N'PREG-0001',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = N'Deben ser retirados todos los restos una vez procesada la op',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0058';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0058', N'FORM-0004', N'PREG-0001', N'No',
        NULL, N'OPC-002', N'Deben ser retirados todos los restos una vez procesada la op', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0059')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0004',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'no todo lo de solvente',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0059';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0059', N'FORM-0004', N'PREG-0002', N'no todo lo de solvente',
        NULL, N'OPC-001', N'retirar lo restante', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0060')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0004',
        [id_pregunta] = N'PREG-0002',
        [respuesta_texto] = N'no todo lo de tinta',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-003',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(NULL, [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0060';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0060', N'FORM-0004', N'PREG-0002', N'no todo lo de tinta',
        NULL, N'OPC-003', N'retirar lo restante', COALESCE(NULL, SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0061')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0005',
        [id_pregunta] = N'PREG-0006',
        [respuesta_texto] = N'Si',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-13 17:27:52', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0061';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0061', N'FORM-0005', N'PREG-0006', N'Si',
        NULL, N'OPC-001', NULL, COALESCE(N'2026-04-13 17:27:52', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0062')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0005',
        [id_pregunta] = N'PREG-0004',
        [respuesta_texto] = N'no todo lo de solvente',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = N'retirar lo restante',
        [fecha_creacion] = COALESCE(N'2026-04-13 17:27:52', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0062';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0062', N'FORM-0005', N'PREG-0004', N'no todo lo de solvente',
        NULL, N'OPC-001', N'retirar lo restante', COALESCE(N'2026-04-13 17:27:52', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0063')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0005',
        [id_pregunta] = N'PREG-0004',
        [respuesta_texto] = N'todo lo de tinta',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-004',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-13 17:27:52', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0063';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0063', N'FORM-0005', N'PREG-0004', N'todo lo de tinta',
        NULL, N'OPC-004', NULL, COALESCE(N'2026-04-13 17:27:52', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0064')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0006',
        [id_pregunta] = N'PREG-0006',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = N'Deben ser retirados todos los restos una vez procesada la op',
        [fecha_creacion] = COALESCE(N'2026-04-13 17:30:27', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0064';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0064', N'FORM-0006', N'PREG-0006', N'No',
        NULL, N'OPC-002', N'Deben ser retirados todos los restos una vez procesada la op', COALESCE(N'2026-04-13 17:30:27', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0065')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0006',
        [id_pregunta] = N'PREG-0004',
        [respuesta_texto] = N'todo de todo',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-005',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-13 17:30:27', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0065';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0065', N'FORM-0006', N'PREG-0004', N'todo de todo',
        NULL, N'OPC-005', NULL, COALESCE(N'2026-04-13 17:30:27', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0066')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0007',
        [id_pregunta] = N'PREG-0006',
        [respuesta_texto] = N'Si',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-001',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-20 14:40:32', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0066';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0066', N'FORM-0007', N'PREG-0006', N'Si',
        NULL, N'OPC-001', NULL, COALESCE(N'2026-04-20 14:40:32', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0067')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0007',
        [id_pregunta] = N'PREG-0004',
        [respuesta_texto] = N'todo de todo',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-005',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-20 14:40:32', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0067';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0067', N'FORM-0007', N'PREG-0004', N'todo de todo',
        NULL, N'OPC-005', NULL, COALESCE(N'2026-04-20 14:40:32', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0068')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0047',
        [id_pregunta] = N'PREG-0006',
        [respuesta_texto] = N'No',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-002',
        [accion_correctiva_aplicada] = N'Deben ser retirados todos los restos una vez procesada la op',
        [fecha_creacion] = COALESCE(N'2026-04-20 14:55:16', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0068';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0068', N'FORM-0047', N'PREG-0006', N'No',
        NULL, N'OPC-002', N'Deben ser retirados todos los restos una vez procesada la op', COALESCE(N'2026-04-20 14:55:16', SYSDATETIME())
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[respuestas_formulario] WHERE [id_respuesta] = N'RESP-0069')
BEGIN
    UPDATE [dbo].[respuestas_formulario]
    SET
        [id_formulario] = N'FORM-0047',
        [id_pregunta] = N'PREG-0004',
        [respuesta_texto] = N'todo de todo',
        [respuesta_numero] = NULL,
        [id_opcion] = N'OPC-005',
        [accion_correctiva_aplicada] = NULL,
        [fecha_creacion] = COALESCE(N'2026-04-20 14:55:16', [fecha_creacion])
    WHERE [id_respuesta] = N'RESP-0069';
END
ELSE
BEGIN
    INSERT INTO [dbo].[respuestas_formulario] (
        [id_respuesta], [id_formulario], [id_pregunta], [respuesta_texto],
        [respuesta_numero], [id_opcion], [accion_correctiva_aplicada], [fecha_creacion]
    )
    VALUES (
        N'RESP-0069', N'FORM-0047', N'PREG-0004', N'todo de todo',
        NULL, N'OPC-005', NULL, COALESCE(N'2026-04-20 14:55:16', SYSDATETIME())
    );
END;

COMMIT TRANSACTION;
GO

SELECT COUNT(*) AS total_respuestas
FROM [dbo].[respuestas_formulario];
GO

SELECT
    COUNT(*) AS total_acciones_correctivas_derivables
FROM [dbo].[respuestas_formulario] r
LEFT JOIN [dbo].[pregunta_opciones] o
    ON o.[id_pregunta] = r.[id_pregunta]
   AND o.[id_opcion] = r.[id_opcion]
WHERE LTRIM(RTRIM(COALESCE(r.[accion_correctiva_aplicada], o.[accion_correctiva], N''))) <> N'';
GO