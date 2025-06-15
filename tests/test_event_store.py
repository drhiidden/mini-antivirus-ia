import os
import tempfile

from agent.utils.event_bus import Event, EventBus
from agent.utils.event_store import SQLiteEventStore


def test_event_persistence(tmp_path):
    db_file = tmp_path / "events.db"
    store = SQLiteEventStore(db_path=db_file)
    bus = EventBus(store=store)

    ev = Event(event_type="sample", payload={"a": 1})
    bus.publish(ev)

    events = store.get_events("sample")
    assert len(events) == 1
    assert events[0].payload["a"] == 1 