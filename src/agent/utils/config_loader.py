from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config.yaml"

# Cargar variables desde .env si existe
load_dotenv(DEFAULT_CONFIG_PATH.parent.parent / ".env")


def _interpolate(value: Any) -> Any:
    """Reemplaza ${VAR} por valor de entorno si existe."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.getenv(env_var, "") or value  # devuelve vacío si no está definido
    return value


def load_config(path: Path | str | None = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not cfg_path.exists():
        return {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "event_db_path": os.getenv("EVENT_DB_PATH", "events.db"),
            "process_scan_interval": float(os.getenv("PROCESS_SCAN_INTERVAL", 1.5)),
        }

    data = yaml.safe_load(cfg_path.read_text()) or {}
    app_cfg = data.get("app", {})

    return {
        "log_level": _interpolate(app_cfg.get("log_level", os.getenv("LOG_LEVEL", "INFO"))) or "INFO",
        "event_db_path": os.getenv("EVENT_DB_PATH", _interpolate(app_cfg.get("event_db_path", "events.db"))),
        "process_scan_interval": float(
            os.getenv(
                "PROCESS_SCAN_INTERVAL",
                _interpolate(app_cfg.get("process_scan_interval", 1.5)),
            )
        ),
    } 