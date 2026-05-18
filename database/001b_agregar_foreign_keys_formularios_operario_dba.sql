-- Comentario CDLform: script SQL de instalacion/migracion; revisar antes de ejecutar en una base real.
-- No forma parte del flujo runtime diario de gestion, operario o MQTT.

USE [MetricsBetaProductivo];
GO

ALTER TABLE [dbo].[pregunta_opciones]
ADD CONSTRAINT [FK_pregunta_opciones_preguntas]
FOREIGN KEY ([id_pregunta])
REFERENCES [dbo].[preguntas] ([id_pregunta]);
GO

ALTER TABLE [dbo].[plantilla_preguntas_items]
ADD CONSTRAINT [FK_plantilla_preguntas_items_plantillas]
FOREIGN KEY ([id_plantilla])
REFERENCES [dbo].[plantillas_preguntas] ([id_plantilla]);
GO

ALTER TABLE [dbo].[plantilla_preguntas_items]
ADD CONSTRAINT [FK_plantilla_preguntas_items_preguntas]
FOREIGN KEY ([id_pregunta])
REFERENCES [dbo].[preguntas] ([id_pregunta]);
GO

ALTER TABLE [dbo].[formularios_operario]
ADD CONSTRAINT [FK_formularios_operario_plantillas]
FOREIGN KEY ([id_plantilla_preguntas])
REFERENCES [dbo].[plantillas_preguntas] ([id_plantilla]);
GO

ALTER TABLE [dbo].[respuestas_formulario]
ADD CONSTRAINT [FK_respuestas_formulario_formularios]
FOREIGN KEY ([id_formulario])
REFERENCES [dbo].[formularios_operario] ([id_formulario]);
GO

ALTER TABLE [dbo].[respuestas_formulario]
ADD CONSTRAINT [FK_respuestas_formulario_preguntas]
FOREIGN KEY ([id_pregunta])
REFERENCES [dbo].[preguntas] ([id_pregunta]);
GO

ALTER TABLE [dbo].[respuestas_formulario]
ADD CONSTRAINT [FK_respuestas_formulario_opciones]
FOREIGN KEY ([id_pregunta], [id_opcion])
REFERENCES [dbo].[pregunta_opciones] ([id_pregunta], [id_opcion]);
GO
