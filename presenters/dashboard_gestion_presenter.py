"""Capa presenter que conecta vistas PyQt con servicios de negocio.

Este comentario de modulo ayuda a ubicar el archivo dentro del flujo actual sin alterar su logica.
"""

from __future__ import annotations

from ui.admin_preguntas import AdminPreguntasView
from ui.acciones_correctivas import AccionesCorrectivasView
from ui.auditoria_formularios import AuditoriaFormulariosView
from ui.reportes import ReportesView
from ui.usuarios_gestion import UsuariosGestionView
from services.reporting.reporte_service import ReporteService


# Bloque CDLform: clase DashboardGestionPresenter; agrupa estado y comportamiento de esta parte del flujo.
class DashboardGestionPresenter:
    # Bloque CDLform: funcion/metodo __init__; encapsula una operacion del flujo del modulo.
    def __init__(self, reporte_service: ReporteService | None = None) -> None:
        self.reporte_service = reporte_service or ReporteService()

    # Bloque CDLform: funcion/metodo crear_admin_preguntas_view; encapsula una operacion del flujo del modulo.
    def crear_admin_preguntas_view(self) -> AdminPreguntasView:
        return AdminPreguntasView()

    # Bloque CDLform: funcion/metodo crear_reportes_view; encapsula una operacion del flujo del modulo.
    def crear_reportes_view(self) -> ReportesView:
        return ReportesView()

    # Bloque CDLform: funcion/metodo crear_auditoria_formularios_view; encapsula una operacion del flujo del modulo.
    def crear_auditoria_formularios_view(self) -> AuditoriaFormulariosView:
        return AuditoriaFormulariosView()

    # Bloque CDLform: funcion/metodo crear_acciones_correctivas_view; encapsula una operacion del flujo del modulo.
    def crear_acciones_correctivas_view(self) -> AccionesCorrectivasView:
        return AccionesCorrectivasView()

    # Bloque CDLform: funcion/metodo crear_usuarios_gestion_view; encapsula una operacion del flujo del modulo.
    def crear_usuarios_gestion_view(self) -> UsuariosGestionView:
        return UsuariosGestionView()

    # Bloque CDLform: funcion/metodo obtener_metricas_dashboard; encapsula una operacion del flujo del modulo.
    def obtener_metricas_dashboard(self) -> dict:
        return self.reporte_service.obtener_metricas_dashboard()
