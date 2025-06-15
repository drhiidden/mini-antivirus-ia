# Wrapper para lanzar el agente usando `python -m src.scripts.run_agent`
from __future__ import annotations

import sys
from pathlib import Path

# Asegurar que 'src' está en sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from agent.cli import main  # noqa: E402

if __name__ == "__main__":
    main() 