from __future__ import annotations

from datetime import datetime, timedelta

from models.application import Application


def test_added_label_describes_relative_age():
    now = datetime.now()
    assert Application("a", "A", None, now).added_label == "Added just now"
    assert Application("b", "B", None, now - timedelta(minutes=5)).added_label == "Added 5m ago"
    assert Application("c", "C", None, now - timedelta(hours=3)).added_label == "Added 3h ago"
    assert Application("d", "D", None, now - timedelta(days=4)).added_label == "Added 4d ago"
