from __future__ import annotations

import argparse
import inspect
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from ui.login import LoginView
from ui.seleccion_operario import SeleccionOperarioView
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
    errores = []

    if not args.op or not str(args.op).strip():
        errores.append("Falta el parametro --op")

    if not args.area or not str(args.area).strip():
        errores.append("Falta el parametro --area")

    if not args.maquina or not str(args.maquina).strip():
        errores.append("Falta el parametro --maquina")

    return errores


def crear_seleccion_operario_modo_auto(args) -> SeleccionOperarioView:
    kwargs_disponibles = {
        "op": args.op.strip() if args.op else None,
        "area": args.area.strip() if args.area else None,
        "maquina": args.maquina.strip() if args.maquina else None,
        "evento_origen": (
            args.evento_origen.strip()
            if args.evento_origen and str(args.evento_origen).strip()
            else None
        ),
    }
    signature = inspect.signature(SeleccionOperarioView.__init__)
    kwargs_aceptados = {
        nombre: valor
        for nombre, valor in kwargs_disponibles.items()
        if nombre in signature.parameters
    }
    return SeleccionOperarioView(**kwargs_aceptados)


def main() -> None:
    args = parse_args()
    app = QApplication(sys.argv)
    cargar_estilos(app)

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

        ventana = crear_seleccion_operario_modo_auto(args)
        ventana.show()
        sys.exit(app.exec_())

    QMessageBox.critical(None, "Error", "Modo de ejecucion no valido.")
    sys.exit(1)


if __name__ == "__main__":
    main()
