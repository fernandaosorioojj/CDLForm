from __future__ import annotations

import sys
from pathlib import Path

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from main import main


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--modo", "normal"]
    main()
