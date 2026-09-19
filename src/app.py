import os
import sys

from PySide6.QtWidgets import QApplication

from utils.logging_config import configure_logging, get_logger
from views.containers.MainWindow import MainWindow

if __name__ == "__main__":
    configure_logging()
    logger = get_logger(__name__)

    app = QApplication(sys.argv)
    dpi = app.primaryScreen().logicalDotsPerInch()
    os.environ["QT_FONT_DPI"] = str(int(dpi))

    window = MainWindow()
    window.theme.apply(app)
    logger.info("Started %s with theme '%s'", window.settings.get("app_name"), window.theme_name)

    window.show()

    sys.exit(app.exec())
