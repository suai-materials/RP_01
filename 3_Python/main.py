import os
from pathlib import Path
import resources_
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWebEngine import QtWebEngine
from LoaderManager import LoaderManager

if __name__ == "__main__":
    sys.argv += ['--style', 'material']
    QtWebEngine.initialize()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(":/drawable/logo.png"))
    qmlRegisterType(LoaderManager, 'io.integrals.LoaderManager', 1, 0, 'LoaderManager')
    engine = QQmlApplicationEngine()
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
