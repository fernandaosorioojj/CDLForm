from __future__ import annotations

import sys
from pathlib import Path

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from worker_main import main


if __name__ == "__main__":
    raise SystemExit(main())
