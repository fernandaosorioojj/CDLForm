from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from services.forms.formulario_service import FormularioService
from services.forms.operario_service import OperarioService
from ui.seleccion_operario import SeleccionOperarioView
from utils.style_loader import load_qss_files


class FakeApontamentoQueryService:
    def listar_operadores_registrados(
        self,
        patron: str | None = None,
        limit: int | None = None,
    ) -> list[str]:
        operadores = [
            "13059605",
            "PMUNOZ",
            "OPR-001 - Operario Prueba",
            "22334455 - Ana Morales",
            "33445566 - Luis Perez",
            "10000001 - Operador Uno",
            "10000002 - Operador Dos",
            "10000003 - Operador Tres",
        ]

        if patron and patron.strip():
            texto = patron.strip().lower()
            return [operador for operador in operadores if texto in operador.lower()]

        if limit is not None:
            return operadores[:limit]

        return operadores


def cargar_estilos(app: QApplication) -> None:
    app.setStyleSheet(load_qss_files("base.qss", "seleccion_operario.qss"))


def main() -> int:
    app = QApplication(sys.argv)
    cargar_estilos(app)

    usar_operadores_fake = "--fake-operadores" in sys.argv
    formulario_service = FormularioService()
    formulario = formulario_service.obtener_siguiente_formulario_pendiente_operario()

    if formulario is None:
        QMessageBox.information(
            None,
            "Formulario de operario",
            "No hay formularios pendientes para probar.",
        )
        return 0

    if usar_operadores_fake:
        operario_service = OperarioService(
            apontamento_query_service=FakeApontamentoQueryService()
        )
    else:
        operario_service = OperarioService()

    ventana = SeleccionOperarioView(
        formulario=formulario,
        formulario_service=formulario_service,
        operario_service=operario_service,
    )
    ventana.show()

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
