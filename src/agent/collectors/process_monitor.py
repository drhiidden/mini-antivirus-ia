from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, Set

import psutil
import structlog

from agent.utils.event_bus import Event, EventBus
from agent.utils.file_helpers import file_hash, is_file_signed

logger = structlog.get_logger(__name__)


@dataclass
class ProcessInfo:
    pid: int
    name: str
    exe: str
    username: str
    cmdline: str
    sha256: str
    is_signed: bool
    parent_pid: int


class ProcessMonitor(threading.Thread):
    """Hilo que monitoriza procesos y publica eventos cuando detecta uno nuevo."""

    def __init__(
        self,
        bus: EventBus,
        interval: float = 2.0,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.bus = bus
        self.interval = interval
        self.daemon = True  # Termina con el programa principal
        self._stop_event = threading.Event()
        self._known_pids: Set[int] = set()

    def run(self) -> None:  # pragma: no cover
        logger.info("ProcessMonitor iniciado", interval=self.interval)
        while not self._stop_event.is_set():
            self.scan()
            time.sleep(self.interval)

    def stop(self) -> None:
        self._stop_event.set()

    # --- Lógica principal ---

    def scan(self) -> None:
        """Analiza los procesos activos y publica eventos por nuevos procesos."""

        current_pids = set(psutil.pids())

        # Nuevos procesos = diferencia entre actual y conocidos
        new_pids = current_pids - self._known_pids
        self._known_pids = current_pids

        for pid in new_pids:
            try:
                proc = psutil.Process(pid)
                info = ProcessInfo(
                    pid=pid,
                    name=proc.name(),
                    exe=proc.exe() or "",
                    username=proc.username() or "",
                    cmdline=" ".join(proc.cmdline()) if proc.cmdline() else "",
                    sha256=file_hash(proc.exe()) if proc.exe() else "",
                    is_signed=is_file_signed(proc.exe()) if proc.exe() else False,
                    parent_pid=proc.ppid() or 0,
                )
                self.publish_new_process(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # El proceso terminó o no hay permisos para inspeccionarlo
                continue

    def publish_new_process(self, info: ProcessInfo) -> None:
        event = Event(
            event_type="process_created",
            payload={
                "pid": info.pid,
                "name": info.name,
                "exe": info.exe,
                "username": info.username,
                "cmdline": info.cmdline,
                "sha256": info.sha256,
                "is_signed": info.is_signed,
                "parent_pid": info.parent_pid,
            },
        )
        logger.debug("Nuevo proceso detectado", pid=info.pid, name=info.name)
        self.bus.publish(event) 