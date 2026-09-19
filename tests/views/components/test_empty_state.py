from views.components.EmptyState import EmptyState


def test_empty_state_builds(qtbot):
    empty_state = EmptyState(title="Nothing", description="Try again")
    qtbot.addWidget(empty_state)
    assert empty_state.objectName() == "emptyState"
