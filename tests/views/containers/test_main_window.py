from configs.Settings import Settings
from views.containers.AppShell import AppShell
from views.containers.MainWindow import MainWindow
from views.widgets.Sidebar import Sidebar, SidebarItem
from views.widgets.TitleBar import TitleBar


# NOTE: an integration test that also asserts on TitleBar, Sidebar and AppShell;
# kept whole to preserve the original assertions.
def test_main_window_hosts_app_shell_chrome(qtbot):
    settings = Settings().items

    title_bar = TitleBar(name="titlebar", parent=None, settings=settings)
    sidebar = Sidebar(name="sidebar", parent=None, settings=settings)
    shell = AppShell(name="appshell", settings=settings)
    window = MainWindow()

    qtbot.addWidget(title_bar)
    qtbot.addWidget(sidebar)
    qtbot.addWidget(shell)
    qtbot.addWidget(window)

    assert title_bar.title_label.text() == settings["app_name"]
    assert isinstance(sidebar, Sidebar)
    assert isinstance(shell, AppShell)
    assert isinstance(window.centralWidget(), AppShell)
    assert shell.stacked_widget is not None
    assert isinstance(sidebar.items[0], SidebarItem)
