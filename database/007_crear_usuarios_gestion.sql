IF OBJECT_ID(N'[dbo].[usuarios_gestion]', N'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[usuarios_gestion] (
        [id_usuario]       INT IDENTITY(1,1) NOT NULL,
        [usuario]          NVARCHAR(100) NOT NULL,
        [password_hash]    NVARCHAR(300) NOT NULL,
        [rol]              NVARCHAR(50)  NOT NULL CONSTRAINT [DF_usuarios_gestion_rol] DEFAULT (N'gestion'),
        [activo]           BIT NOT NULL CONSTRAINT [DF_usuarios_gestion_activo] DEFAULT (1),
        [fecha_creacion]   DATETIME2(0) NOT NULL CONSTRAINT [DF_usuarios_gestion_fecha_creacion] DEFAULT (SYSDATETIME()),
        [fecha_actualizacion] DATETIME2(0) NOT NULL CONSTRAINT [DF_usuarios_gestion_fecha_actualizacion] DEFAULT (SYSDATETIME()),
        CONSTRAINT [PK_usuarios_gestion] PRIMARY KEY CLUSTERED ([id_usuario]),
        CONSTRAINT [UX_usuarios_gestion_usuario] UNIQUE ([usuario])
    );
END;
GO

IF COL_LENGTH(N'[dbo].[usuarios_gestion]', N'rol') IS NULL
BEGIN
    ALTER TABLE [dbo].[usuarios_gestion]
    ADD [rol] NVARCHAR(50) NOT NULL
        CONSTRAINT [DF_usuarios_gestion_rol] DEFAULT (N'gestion')
        WITH VALUES;
END;
GO

UPDATE [dbo].[usuarios_gestion]
SET
    [rol] = N'gestion',
    [fecha_actualizacion] = SYSDATETIME()
WHERE [rol] NOT IN (N'admin', N'gestion');
GO

-- Para crear un usuario, genere primero el hash con:
-- python -c "from services.security.auth_service import AuthService; print(AuthService.generar_password_hash('TU_PASSWORD'))"
--
-- Luego inserte o actualice:
-- MERGE [dbo].[usuarios_gestion] AS target
-- USING (SELECT N'admin' AS [usuario], N'pbkdf2_sha256$260000$SALT_HEX$HASH_HEX' AS [password_hash], N'admin' AS [rol]) AS source
-- ON target.[usuario] = source.[usuario]
-- WHEN MATCHED THEN
--     UPDATE SET
--         [password_hash] = source.[password_hash],
--         [rol] = source.[rol],
--         [activo] = 1,
--         [fecha_actualizacion] = SYSDATETIME()
-- WHEN NOT MATCHED THEN
--     INSERT ([usuario], [password_hash], [rol], [activo])
--     VALUES (source.[usuario], source.[password_hash], source.[rol], 1);
-- GO
