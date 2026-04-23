from __future__ import annotations

from ui.admin_preguntas import AdminPreguntasView
from ui.acciones_correctivas import AccionesCorrectivasView
from ui.auditoria_formularios import AuditoriaFormulariosView
from ui.reportes import ReportesView
from ui.usuarios_gestion import UsuariosGestionView
from services.reporting.reporte_service import ReporteService


class DashboardGestionPresenter:
    def __init__(self, reporte_service: ReporteService | None = None) -> None:
        self.reporte_service = reporte_service or ReporteService()

    def crear_admin_preguntas_view(self) -> AdminPreguntasView:
        return AdminPreguntasView()

    def crear_reportes_view(self) -> ReportesView:
        return ReportesView()

    def crear_auditoria_formularios_view(self) -> AuditoriaFormulariosView:
        return AuditoriaFormulariosView()

    def crear_acciones_correctivas_view(self) -> AccionesCorrectivasView:
        return AccionesCorrectivasView()

    def crear_usuarios_gestion_view(self) -> UsuariosGestionView:
        return UsuariosGestionView()

    def obtener_metricas_dashboard(self) -> dict:
        return self.reporte_service.obtener_metricas_dashboard()
