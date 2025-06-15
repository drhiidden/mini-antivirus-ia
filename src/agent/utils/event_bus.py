from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, DefaultDict, Dict, List

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class Event:
    """Representa un evento genérico dentro del sistema."""

    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Event type={self.event_type} payload={self.payload}>"


class EventBus:
    """Sistema sencillo de publicación/suscripción (pub-sub) con persistencia opcional."""

    _subscribers: DefaultDict[str, List[Callable[[Event], None]]]
    _lock: threading.Lock
    _store: "SQLiteEventStore | None"

    def __init__(self, store: "SQLiteEventStore | None" = None) -> None:
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()
        self._store = store
        logger.debug("EventBus inicializado", persistence=bool(store))

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """Registra un handler para un tipo de evento."""

        with self._lock:
            self._subscribers[event_type].append(handler)
            logger.debug("Handler suscrito", event_type=event_type, handler=handler)

    def publish(self, event: Event) -> None:
        """Publica un evento a todos los suscriptores."""

        with self._lock:
            handlers = list(self._subscribers.get(event.event_type, []))

        logger.debug(
            "Evento publicado", event_type=event.event_type, handler_count=len(handlers)
        )
        # Persistencia opcional
        if self._store is not None:
            try:
                self._store.save_event(event)
            except Exception as exc:  # pragma: no cover
                logger.exception("Error al persistir evento", exc_info=exc)

        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:  # pragma: no cover
                logger.exception("Error en handler de evento", exc_info=exc) 