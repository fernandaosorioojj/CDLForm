from __future__ import annotations

import argparse
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from integrations.event_processor import EventProcessor
from launcher.app_launcher import AppLauncher
from launcher.pending_form_coordinator import PendingFormCoordinator
from ui.login import LoginView
from utils.style_loader import load_qss_files


def cargar_estilos(app: QApplication) -> None:
    app.setStyleSheet(load_qss_files("base.qss"))


def parse_args():
    parser = argparse.ArgumentParser(description="CDLform")

    parser.add_argument(
        "--modo",
        choices=["normal", "auto"],
        default="normal",
        help="Modo de ejecucion de la aplicacion",
    )

    parser.add_argument("--op", default=None, help="OP asociada al formulario")
    parser.add_argument("--area", default=None, help="Area asociada al formulario")
    parser.add_argument("--maquina", default=None, help="Maquina asociada al formulario")
    parser.add_argument(
        "--evento-origen",
        dest="evento_origen",
        default=None,
        help="ID o referencia del evento origen",
    )

    return parser.parse_args()


def validar_argumentos_modo_auto(args) -> list[str]:
    return []


def construir_mensaje_sin_formulario(resultado: dict) -> str:
    contexto = resultado.get("contexto", {})
    recursos = contexto.get("cod_recursos", [])
    recursos_texto = ", ".join(str(recurso) for recurso in recursos) or "sin recursos"

    lineas = [
        "No hay formularios pendientes para abrir.",
        "",
        f"Origen: {resultado.get('origen_sincronizacion', 'desconocido')}",
        f"Estacion: {contexto.get('estacion') or 'sin estacion'}",
        f"Recursos consultados: {recursos_texto}",
        f"Eventos consultados: {resultado.get('total_consultados', 0)}",
        f"Formularios creados: {resultado.get('total_formularios_creados', 0)}",
        f"Formularios existentes pendientes: {resultado.get('total_formularios_existentes', 0)}",
        f"Omitidos ya cerrados/localmente procesados: {resultado.get('total_omitidos_ya_procesados', 0)}",
        f"Omitidos sin NumOrdem: {resultado.get('total_omitidos_sin_num_ordem', 0)}",
        f"Errores: {resultado.get('total_errores_formulario', 0)}",
    ]

    errores = resultado.get("errores", [])
    if errores:
        primer_error = errores[0]
        lineas.extend(
            [
                "",
                "Primer error:",
                str(primer_error.get("error") or primer_error),
            ]
        )

    return "\n".join(lineas)


def main() -> None:
    args = parse_args()
    app = QApplication(sys.argv)
    cargar_estilos(app)
    app.formulario_launcher = AppLauncher()
    app.pending_form_coordinator = PendingFormCoordinator(
        formulario_launcher=app.formulario_launcher,
    )

    if args.modo == "normal":
        ventana = LoginView()
        ventana.show()
        sys.exit(app.exec_())

    if args.modo == "auto":
        errores = validar_argumentos_modo_auto(args)

        if errores:
            QMessageBox.critical(
                None,
                "Error de ejecucion",
                "No se puede iniciar la aplicacion en modo automatico.\n\n"
                + "\n".join(errores),
            )
            sys.exit(1)

        try:
            app.event_processor_operario = EventProcessor()
            resultado = app.event_processor_operario.procesar_evento_externo(
                evento={
                    "op": args.op,
                    "area": args.area,
                    "maquina": args.maquina,
                    "evento_origen": args.evento_origen,
                },
                usar_fallback_consulta=False,
            )
        except Exception as exc:
            QMessageBox.critical(
                None,
                "Error de ejecucion",
                f"No se pudo procesar la cola de formularios.\n\n{exc}",
            )
            sys.exit(1)

        resultado_apertura = app.pending_form_coordinator.revisar_pendientes()
        if not resultado_apertura.get("se_preparo"):
            QMessageBox.information(
                None,
                "Formulario",
                construir_mensaje_sin_formulario(resultado),
            )
            sys.exit(0)

        sys.exit(app.exec_())

    QMessageBox.critical(None, "Error", "Modo de ejecucion no valido.")
    sys.exit(1)


if __name__ == "__main__":
    main()
