from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from agent.utils.event_bus import Event


class SQLiteEventStore:
    """Almacena eventos en una base SQLite simple."""

    def __init__(self, db_path: str | Path = "events.db") -> None:
        self.db_path = Path(db_path)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()

    # ---------------------------------------------------------------------
    # API pública
    # ---------------------------------------------------------------------

    def save_event(self, event: Event) -> None:
        """Guarda un evento en la base de datos."""
        with self._conn:  # maneja commit automáticamente
            self._conn.execute(
                """
                INSERT INTO events (event_type, payload, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    event.event_type,
                    json.dumps(event.payload, ensure_ascii=False),
                    event.created_at.isoformat(),
                ),
            )

    def get_events(self, event_type: Optional[str] = None) -> List[Event]:
        """Recupera eventos opcionalmente filtrados por tipo."""
        cursor = self._conn.cursor()
        if event_type:
            cursor.execute(
                "SELECT event_type, payload, created_at FROM events WHERE event_type = ?",
                (event_type,),
            )
        else:
            cursor.execute("SELECT event_type, payload, created_at FROM events")

        rows = cursor.fetchall()
        events: List[Event] = []
        for row in rows:
            events.append(
                Event(
                    event_type=row["event_type"],
                    payload=json.loads(row["payload"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
            )
        return events

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _create_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def close(self) -> None:
        self._conn.close()