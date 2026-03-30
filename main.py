from __future__ import annotations

import sys
import argparse

from PyQt5.QtWidgets import QApplication, QMessageBox

from ui.login import LoginView
from ui.seleccion_operario import SeleccionOperarioView


def parse_args():
    parser = argparse.ArgumentParser(description="CDLform")

    parser.add_argument(
        "--modo",
        choices=["normal", "auto"],
        default="normal",
        help="Modo de ejecución de la aplicación",
    )

    parser.add_argument("--op", default=None, help="OP asociada al formulario")
    parser.add_argument("--area", default=None, help="Área asociada al formulario")
    parser.add_argument("--maquina", default=None, help="Máquina asociada al formulario")
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
        errores.append("Falta el parámetro --op")

    if not args.area or not str(args.area).strip():
        errores.append("Falta el parámetro --area")

    if not args.maquina or not str(args.maquina).strip():
        errores.append("Falta el parámetro --maquina")

    return errores


def main():
    args = parse_args()
    app = QApplication(sys.argv)

    if args.modo == "normal":
        ventana = LoginView()
        ventana.show()
        sys.exit(app.exec_())

    if args.modo == "auto":
        errores = validar_argumentos_modo_auto(args)

        if errores:
            QMessageBox.critical(
                None,
                "Error de ejecución",
                "No se puede iniciar la aplicación en modo automático.\n\n"
                + "\n".join(errores),
            )
            sys.exit(1)

        ventana = SeleccionOperarioView(
            op=args.op.strip(),
            area=args.area.strip(),
            maquina=args.maquina.strip(),
            evento_origen=args.evento_origen.strip()
            if args.evento_origen and str(args.evento_origen).strip()
            else None,
        )
        ventana.show()
        sys.exit(app.exec_())

    QMessageBox.critical(None, "Error", "Modo de ejecución no válido.")
    sys.exit(1)


if __name__ == "__main__":
    main()