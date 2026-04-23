from __future__ import annotations

import argparse
import json
import sys

from integrations.event_processor import EventProcessor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CDLform worker")
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


def main() -> int:
    args = parse_args()
    event_processor = EventProcessor()

    resultado = event_processor.procesar_evento_externo(
        evento={
            "op": args.op,
            "area": args.area,
            "maquina": args.maquina,
            "evento_origen": args.evento_origen,
        },
    )

    sys.stdout.write(json.dumps(resultado, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
