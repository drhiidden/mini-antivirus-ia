from __future__ import annotations

import os
import time
from pathlib import Path

from agent.collectors.process_monitor import ProcessMonitor
from agent.utils.event_bus import EventBus
from agent.utils.event_store import SQLiteEventStore
from agent.utils.logger_config import setup_logging
from agent.utils.config_loader import load_config


def main() -> None:  # pragma: no cover
    """Punto de entrada CLI: `poetry run minia`."""

    # Leer configuración de entorno
    cfg = load_config()
    log_level = cfg["log_level"]
    db_path = Path(cfg["event_db_path"])
    scan_interval = cfg["process_scan_interval"]

    # Asegurar carpeta de datos
    db_path.parent.mkdir(parents=True, exist_ok=True)

    setup_logging(log_level)

    store = SQLiteEventStore(db_path=db_path)
    bus = EventBus(store=store)

    bus.subscribe(
        "process_created",
        lambda e: None,  # Punto de enganche para análisis / alertas
    )

    monitor = ProcessMonitor(bus=bus, interval=scan_interval)
    monitor.start()

    print(
        f"[MiniAntivirus-IA] Ejecutando. Base de datos: {db_path} | Intervalo: {scan_interval}s"
    )
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        monitor.stop()
        print("\n[MiniAntivirus-IA] Monitor detenido") 