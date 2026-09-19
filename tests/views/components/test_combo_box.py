from views.components.ComboBox import ComboBox
from views.components.TextInput import TextInput


# NOTE: also covers TextInput; kept as one test to preserve the original assertions.
def test_combo_box_and_text_input_build(qtbot):
    combo = ComboBox(items=["Default", "Dracula"], current="Dracula")
    qtbot.addWidget(combo)
    assert combo.currentText() == "Dracula"

    text_input = TextInput(placeholder="Type here", text="hello")
    qtbot.addWidget(text_input)
    assert text_input.text() == "hello"
    assert text_input.placeholderText() == "Type here"
