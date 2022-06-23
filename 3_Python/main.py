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
from GeneratorManager import GeneratorManager

if __name__ == "__main__":
    sys.argv += ['--style', 'material']
    QtWebEngine.initialize()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(":/drawable/logo.png"))
    qmlRegisterType(LoaderManager, 'io.integrals.api', 1, 0, 'LoaderManager')
    qmlRegisterType(GeneratorManager, 'io.integrals.api', 1, 0, 'GeneratorManager')
    engine = QQmlApplicationEngine()
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
