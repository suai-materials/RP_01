import threading
from threading import Thread
import requests

from PySide2.QtCore import QObject, Slot, Signal, Property
from time import sleep


class LoaderManager(QObject):
    frame_changed = Signal(str)
    auth_visible_changed = Signal(bool)
    _frame_now = "./splash.qml"
    _auth_visible = False

    def __init__(self, parent=None):
        super().__init__(parent)
        threading.Thread(target=check_connection, args=(self,)).start()

    def get_frame_now(self):
        return self._frame_now

    def get_auth_visible(self):
        return self._auth_visible

    @Slot(str)
    def set_frame_now(self, frame: str):
        self.set_auth_visible(frame == "./auth.qml")
        self._frame_now = frame
        self.frame_changed.emit(frame)

    @Slot(bool)
    def set_auth_visible(self, isvisible: bool):
        self._auth_visible = isvisible
        self.auth_visible_changed.emit(isvisible)

    frame_now = Property(str, get_frame_now, set_frame_now, notify=frame_changed)
    auth_visible = Property(bool, get_auth_visible, set_auth_visible, notify=auth_visible_changed)


def check_connection(loaderManager: LoaderManager):
    response = requests.get("https://pank.su")
    if response.status_code == 200:
        sleep(2)
        loaderManager.frame_now = "./auth.qml"
