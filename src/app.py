import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from views.containers.MainWindow import MainWindow

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    dpi = app.primaryScreen().logicalDotsPerInch()
    os.environ["QT_FONT_DPI"] = str(int(dpi))
    # app.setWindowIcon(QIcon("resource/favicon.ico"))
    window = MainWindow()
    # window.show()

    sys.exit(app.exec())