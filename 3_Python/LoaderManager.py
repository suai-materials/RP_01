import threading
import requests

from PySide2.QtCore import QObject, Slot, Signal, Property
from time import sleep


class LoaderManager(QObject):
    frame_changed = Signal(str)
    _frame_now = "./splash.qml"

    def __init__(self, parent=None):
        super().__init__(parent)
        threading.Thread(target=check_connection, args=(self,)).start()

    def get_frame_now(self):
        return self._frame_now

    @Slot(str)
    def set_frame_now(self, frame: str):
        self._frame_now = frame
        self.frame_changed.emit(frame)

    frame_now = Property(str, get_frame_now, set_frame_now, notify=frame_changed)


def check_connection(loader_manager: LoaderManager):
    try:
        sleep(1)
        response = requests.get("https://pank.su")
        if response.status_code == 200:
            loader_manager.frame_now = "./auth.qml"
        else:
            raise requests.exceptions.ConnectionError
    except requests.exceptions.ConnectionError:
        loader_manager.frame_now = "./error.qml"
