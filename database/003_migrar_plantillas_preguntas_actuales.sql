USE [MetricsBetaProductivo];
GO

SET XACT_ABORT ON;
GO

BEGIN TRANSACTION;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V001')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 1,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 09:28:58', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 10:49:45'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V001', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        1, 0, COALESCE(N'2026-04-13 09:28:58', SYSDATETIME()), N'2026-04-13 10:49:45'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V001' AND [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V001'
      AND [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V001', N'PREG-0001', 1);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V002')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 2,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 10:49:45', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 10:50:26'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V002';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V002', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        2, 0, COALESCE(N'2026-04-13 10:49:45', SYSDATETIME()), N'2026-04-13 10:50:26'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V002' AND [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V002'
      AND [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V002', N'PREG-0001', 1);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V003')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 3,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 10:50:26', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 10:50:30'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V003';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V003', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        3, 0, COALESCE(N'2026-04-13 10:50:26', SYSDATETIME()), N'2026-04-13 10:50:30'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V003' AND [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V003'
      AND [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V003', N'PREG-0001', 1);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V004')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 4,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 10:50:30', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 10:53:06'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V004', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        4, 0, COALESCE(N'2026-04-13 10:50:30', SYSDATETIME()), N'2026-04-13 10:53:06'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V004' AND [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V004'
      AND [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V004', N'PREG-0001', 1);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 5,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 10:53:06', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 10:57:49'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V005', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        5, 0, COALESCE(N'2026-04-13 10:53:06', SYSDATETIME()), N'2026-04-13 10:57:49'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005' AND [id_pregunta] = N'PREG-0001')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005'
      AND [id_pregunta] = N'PREG-0001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V005', N'PREG-0001', 1);
END;
IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005' AND [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 2
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V005'
      AND [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V005', N'PREG-0004', 2);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V006')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 6,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 10:57:49', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 11:06:20'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V006', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        6, 0, COALESCE(N'2026-04-13 10:57:49', SYSDATETIME()), N'2026-04-13 11:06:20'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V006' AND [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 2
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V006'
      AND [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V006', N'PREG-0004', 2);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 7,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 11:06:20', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-13 15:21:20'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V007', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        7, 0, COALESCE(N'2026-04-13 11:06:20', SYSDATETIME()), N'2026-04-13 15:21:20'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007' AND [id_pregunta] = N'PREG-0006')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007'
      AND [id_pregunta] = N'PREG-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V007', N'PREG-0006', 1);
END;
IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007' AND [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 2
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V007'
      AND [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V007', N'PREG-0004', 2);
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 8,
        [activa] = 0,
        [fecha_creacion] = COALESCE(N'2026-04-13 15:21:20', [fecha_creacion]),
        [fecha_desactivacion] = N'2026-04-20 16:21:39'
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V008', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        8, 0, COALESCE(N'2026-04-13 15:21:20', SYSDATETIME()), N'2026-04-20 16:21:39'
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008' AND [id_pregunta] = N'PREG-0006')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008'
      AND [id_pregunta] = N'PREG-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V008', N'PREG-0006', 1);
END;
IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008' AND [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 2
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V008'
      AND [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V008', N'PREG-0004', 2);
END;

UPDATE [dbo].[plantillas_preguntas]
SET
    [activa] = 0,
    [fecha_desactivacion] = COALESCE([fecha_desactivacion], SYSDATETIME())
WHERE [cod_recurso] = N'UTECO'
  AND [cod_setor] = N'EXTRUSION'
  AND [id_plantilla] <> N'TPL-EXTRUSION-UTECO-V001'
  AND [activa] = 1;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-EXTRUSION-UTECO-V001')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-EXTRUSION-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'EXTRUSION',
        [version] = 1,
        [activa] = 1,
        [fecha_creacion] = COALESCE(N'2026-04-17 10:16:09', [fecha_creacion]),
        [fecha_desactivacion] = NULL
    WHERE [id_plantilla] = N'TPL-EXTRUSION-UTECO-V001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-EXTRUSION-UTECO-V001', N'TPL-EXTRUSION-UTECO', N'UTECO', N'EXTRUSION',
        1, 1, COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()), NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-EXTRUSION-UTECO-V001' AND [id_pregunta] = N'PREG-0009')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 6
    WHERE [id_plantilla] = N'TPL-EXTRUSION-UTECO-V001'
      AND [id_pregunta] = N'PREG-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-EXTRUSION-UTECO-V001', N'PREG-0009', 6);
END;

UPDATE [dbo].[plantillas_preguntas]
SET
    [activa] = 0,
    [fecha_desactivacion] = COALESCE([fecha_desactivacion], SYSDATETIME())
WHERE [cod_recurso] = N'UTECO'
  AND [cod_setor] = N'FOOD_SERVICE'
  AND [id_plantilla] <> N'TPL-FOOD_SERVICE-UTECO-V001'
  AND [activa] = 1;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-FOOD_SERVICE-UTECO-V001')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-FOOD_SERVICE-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'FOOD_SERVICE',
        [version] = 1,
        [activa] = 1,
        [fecha_creacion] = COALESCE(N'2026-04-17 10:16:09', [fecha_creacion]),
        [fecha_desactivacion] = NULL
    WHERE [id_plantilla] = N'TPL-FOOD_SERVICE-UTECO-V001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-FOOD_SERVICE-UTECO-V001', N'TPL-FOOD_SERVICE-UTECO', N'UTECO', N'FOOD_SERVICE',
        1, 1, COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()), NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-FOOD_SERVICE-UTECO-V001' AND [id_pregunta] = N'PREG-0009')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 6
    WHERE [id_plantilla] = N'TPL-FOOD_SERVICE-UTECO-V001'
      AND [id_pregunta] = N'PREG-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-FOOD_SERVICE-UTECO-V001', N'PREG-0009', 6);
END;

UPDATE [dbo].[plantillas_preguntas]
SET
    [activa] = 0,
    [fecha_desactivacion] = COALESCE([fecha_desactivacion], SYSDATETIME())
WHERE [cod_recurso] = N'UTECO'
  AND [cod_setor] = N'IMP_FLEXO'
  AND [id_plantilla] <> N'TPL-IMP_FLEXO-UTECO-V001'
  AND [activa] = 1;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_FLEXO-UTECO-V001')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_FLEXO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_FLEXO',
        [version] = 1,
        [activa] = 1,
        [fecha_creacion] = COALESCE(N'2026-04-17 10:16:09', [fecha_creacion]),
        [fecha_desactivacion] = NULL
    WHERE [id_plantilla] = N'TPL-IMP_FLEXO-UTECO-V001';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_FLEXO-UTECO-V001', N'TPL-IMP_FLEXO-UTECO', N'UTECO', N'IMP_FLEXO',
        1, 1, COALESCE(N'2026-04-17 10:16:09', SYSDATETIME()), NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_FLEXO-UTECO-V001' AND [id_pregunta] = N'PREG-0009')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 6
    WHERE [id_plantilla] = N'TPL-IMP_FLEXO-UTECO-V001'
      AND [id_pregunta] = N'PREG-0009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_FLEXO-UTECO-V001', N'PREG-0009', 6);
END;

UPDATE [dbo].[plantillas_preguntas]
SET
    [activa] = 0,
    [fecha_desactivacion] = COALESCE([fecha_desactivacion], SYSDATETIME())
WHERE [cod_recurso] = N'UTECO'
  AND [cod_setor] = N'IMP_HUEGO'
  AND [id_plantilla] <> N'TPL-IMP_HUEGO-UTECO-V009'
  AND [activa] = 1;

IF EXISTS (SELECT 1 FROM [dbo].[plantillas_preguntas] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009')
BEGIN
    UPDATE [dbo].[plantillas_preguntas]
    SET
        [clave_plantilla] = N'TPL-IMP_HUEGO-UTECO',
        [cod_recurso] = N'UTECO',
        [cod_setor] = N'IMP_HUEGO',
        [version] = 9,
        [activa] = 1,
        [fecha_creacion] = COALESCE(N'2026-04-20 16:21:39', [fecha_creacion]),
        [fecha_desactivacion] = NULL
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantillas_preguntas] (
        [id_plantilla], [clave_plantilla], [cod_recurso], [cod_setor],
        [version], [activa], [fecha_creacion], [fecha_desactivacion]
    )
    VALUES (
        N'TPL-IMP_HUEGO-UTECO-V009', N'TPL-IMP_HUEGO-UTECO', N'UTECO', N'IMP_HUEGO',
        9, 1, COALESCE(N'2026-04-20 16:21:39', SYSDATETIME()), NULL
    );
END;

IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009' AND [id_pregunta] = N'PREG-0006')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 1
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009'
      AND [id_pregunta] = N'PREG-0006';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V009', N'PREG-0006', 1);
END;
IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009' AND [id_pregunta] = N'PREG-0004')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 2
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009'
      AND [id_pregunta] = N'PREG-0004';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V009', N'PREG-0004', 2);
END;
IF EXISTS (SELECT 1 FROM [dbo].[plantilla_preguntas_items] WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009' AND [id_pregunta] = N'PREG-0010')
BEGIN
    UPDATE [dbo].[plantilla_preguntas_items]
    SET [orden] = 20
    WHERE [id_plantilla] = N'TPL-IMP_HUEGO-UTECO-V009'
      AND [id_pregunta] = N'PREG-0010';
END
ELSE
BEGIN
    INSERT INTO [dbo].[plantilla_preguntas_items] (
        [id_plantilla], [id_pregunta], [orden]
    )
    VALUES (N'TPL-IMP_HUEGO-UTECO-V009', N'PREG-0010', 20);
END;

COMMIT TRANSACTION;
GO

SELECT
    (SELECT COUNT(*) FROM [dbo].[plantillas_preguntas]) AS total_plantillas,
    (SELECT COUNT(*) FROM [dbo].[plantilla_preguntas_items]) AS total_items;
GO

SELECT
    [cod_setor],
    [cod_recurso],
    COUNT(*) AS plantillas_activas
FROM [dbo].[plantillas_preguntas]
WHERE [activa] = 1
GROUP BY [cod_setor], [cod_recurso]
ORDER BY [cod_setor], [cod_recurso];
GO