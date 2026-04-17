from __future__ import annotations

from ui.admin_preguntas import AdminPreguntasView
from ui.acciones_correctivas import AccionesCorrectivasView
from ui.auditoria_formularios import AuditoriaFormulariosView
from ui.reportes import ReportesView


class DashboardGestionPresenter:
    def crear_admin_preguntas_view(self) -> AdminPreguntasView:
        return AdminPreguntasView()

    def crear_reportes_view(self) -> ReportesView:
        return ReportesView()

    def crear_auditoria_formularios_view(self) -> AuditoriaFormulariosView:
        return AuditoriaFormulariosView()

    def crear_acciones_correctivas_view(self) -> AccionesCorrectivasView:
        return AccionesCorrectivasView()
