import pytest
from PySide6.QtWidgets import QWidget

from views.components.AnimatedToggle import AnimatedToggle
from views.components.Button import Button
from views.components.Column import Column
from views.components.Row import Row
from views.components.Tooltip import Tooltip
from views.widgets.CreditsBar import CreditsBar
from views.widgets.TitleBar import TitleBar


@pytest.mark.parametrize(
    "widget_factory",
    [
        lambda qtbot: Row(name="row", widgets=[QWidget()]),
        lambda qtbot: Column(name="column", widgets=[QWidget()]),
        lambda qtbot: Button(name="button", label="Test", tooltipLabel="Test tooltip"),
        lambda qtbot: Tooltip(
            name="tooltip",
            parent=None,
            backgroundColor="#000000",
            textColor="#ffffff",
            tooltipText="Hello",
        ),
        lambda qtbot: AnimatedToggle(),
        lambda qtbot: TitleBar(
            name="titlebar", parent=None, settings={"app_name": "PySmartDeskNorm"}
        ),
        lambda qtbot: CreditsBar(
            name="credits", customMessage="Built with PySide6", parent=None, settings={}
        ),
    ],
)
def test_component_smoke(qtbot, widget_factory):
    widget = widget_factory(qtbot)
    qtbot.addWidget(widget)
    assert widget is not None
