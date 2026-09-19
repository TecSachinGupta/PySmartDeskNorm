from views.components.Toast import Toast


def test_toast_shows_and_schedules_hide(qtbot):
    toast = Toast(duration_ms=50)
    qtbot.addWidget(toast)

    toast.show_message("Saved")
    assert toast.text() == "Saved"
    assert toast.isVisible() is True

    qtbot.waitUntil(lambda: not toast.isVisible(), timeout=1000)
