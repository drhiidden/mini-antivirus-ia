import threading
from unittest import mock

import psutil

from agent.collectors.process_monitor import ProcessMonitor
from agent.utils.event_bus import EventBus


def test_process_monitor_scan_new_process(monkeypatch):
    bus = EventBus()
    received = []

    bus.subscribe("process_created", lambda e: received.append(e))

    # Mock psutil.pids and psutil.Process
    monkeypatch.setattr(psutil, "pids", lambda: [1234])

    fake_proc = mock.Mock()
    fake_proc.name.return_value = "malicious.exe"
    fake_proc.exe.return_value = "C:/malicious.exe"
    fake_proc.username.return_value = "user"

    monkeypatch.setattr(psutil, "Process", lambda pid: fake_proc)

    monitor = ProcessMonitor(bus=bus, interval=0.1)
    monitor.scan()

    assert len(received) == 1
    assert received[0].payload["name"] == "malicious.exe" 