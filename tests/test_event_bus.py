from agent.utils.event_bus import Event, EventBus


def test_publish_subscribe():
    bus = EventBus()
    received = {}

    def handler(event: Event):
        received["event"] = event

    bus.subscribe("test_event", handler)
    ev = Event(event_type="test_event", payload={"value": 42})
    bus.publish(ev)

    assert "event" in received
    assert received["event"].payload["value"] == 42 