from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Application:
    """A single tracked application."""

    app_id: str
    name: str
    icon: str | None = None
    added_at: datetime = field(default_factory=datetime.now)

    @property
    def added_label(self) -> str:
        seconds = (datetime.now() - self.added_at).total_seconds()
        if seconds < 60:
            return "Added just now"
        minutes = seconds / 60
        if minutes < 60:
            return f"Added {int(minutes)}m ago"
        hours = minutes / 60
        if hours < 24:
            return f"Added {int(hours)}h ago"
        return f"Added {int(hours / 24)}d ago"
