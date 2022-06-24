import json
import threading
from utils import *

import requests

from PySide2.QtCore import QObject, Slot, Signal, Property
from time import sleep


class LoaderManager(QObject):
    """LoaderManger отвечает за вопросы навигации и запускает функции и потоки в нужный момент"""

    # Информация необходимая нам
    secret_key = ""
    token = ""
    user_data: dict
    io_thread: threading.Thread

    # Сигналы, которые отвечают за уведомление Qt, что что-то произошло, в нашем случае изменение
    # определённой переменной с которой работает qml разметка
    frame_changed = Signal(str)
    nav_visibility_changed = Signal(bool)
    session_id_changed = Signal(int)
    mode_changed = Signal(str)
    header_changed = Signal(str)
    webpage_mode_changed = Signal(str)

    # Приватные переменные
    _session_id = None
    _mode: Mode = Mode.Online
    _frame_now = "splash.qml"
    _nav_visibility = False
    _header = "Темы"
    _webpage_mode = WebPageMode.NotShowing

    def __init__(self, parent=None):
        super().__init__(parent)
        self.io_thread = threading.Thread(target=check_connection, args=(self,))
        self.io_thread.start()

    @Slot(str)
    def set_webpage_mode(self, webpage_mode_str):
        self._webpage_mode = \
            list(filter(lambda webpage_mode: webpage_mode.name == webpage_mode_str, WebPageMode))[0]
        self.webpage_mode_changed.emit(webpage_mode_str)

    def get_webpage_mode(self):
        return self._webpage_mode.name

    @Slot(QObject, str, str, str)
    def open_webpage(self, loader: QObject, url: str, name: str, webpage_mode: str):
        self.webpage_mode = webpage_mode
        if self._webpage_mode == WebPageMode.Test:
            with open("./models/test.html", "w", encoding="utf-8") as test_file:
                test_file.write(requests.get(SERVER_URL + "test/" + url,
                                             headers={"Authorization": self.token}).text)
            loader.setProperty("url", "./models/test.html")
        else:
            loader.setProperty("url", url)
        self.header = name
        self.frame_now = "webpage.qml"

    def get_frame_now(self):
        return self._frame_now

    @Slot(str)
    def set_frame_now(self, frame: str):
        """Смена экранов приложения, SLOT показывает что это setter-свойства qml-элемента"""
        self.nav_visibility = True
        if frame in ["splash.qml", "error.qml", "auth.qml"]:
            self.nav_visibility = False
        if frame == "splash.qml":
            # Запускаем поток, который проверяет интернет соединение
            threading.Thread(target=check_connection, args=(self,)).start()
        elif frame == "topics.qml" and self._mode == Mode.Offline:
            with open("./offline/topics.json", "r", encoding="utf-8") as topics_file:
                topics_json = json.loads(str(topics_file.read()))
                json_to_qml_model(topics_json, "./models/TopicModel.qml")
        elif frame == "profile.qml":
            self.user_data = requests.get(SERVER_URL + "/user_data/",
                                          headers={
                                              "Authorization": self.token}).json()
        self._frame_now = frame
        self.frame_changed.emit(frame)

    def get_nav_visibility(self):
        return self._nav_visibility

    @Slot(bool)
    def set_nav_visibility(self, is_visible: bool):
        self._nav_visibility = is_visible
        self.nav_visibility_changed.emit(is_visible)

    def get_session_id(self):
        return self._session_id

    @Slot(int)
    def set_session_id(self, session_id: int):
        self._session_id = session_id
        self.session_id_changed.emit(session_id)

    def get_mode(self):
        return self._mode.name

    @Slot(str)
    def set_mode(self, mode_str):
        self._mode = list(filter(lambda mode: mode.name == mode_str, Mode))[0]
        self.mode_changed.emit(mode_str)

    def get_header(self):
        return self._header

    @Slot(str)
    def set_header(self, header):
        self._header = header
        self.header_changed.emit(header)

    # Доп. функции для некоторых qml frame'ов
    @Slot()
    def reload(self):
        """Перезагрузка программы"""
        threading.Thread(target=check_connection, args=(self,)).start()
        self.frame_now = "splash.qml"
        self.mode = "Online"

    @Slot()
    def close_test(self):
        requests.post(SERVER_URL + "close_test", headers={"Authorization": self.token})

    @Slot(result=str)
    def get_token(self):
        return self.token

    @Slot(result=str)
    def get_first_name(self):
        return self.user_data["first_name"]

    @Slot(result=str)
    def get_last_name(self):
        if self.user_data["last_name"] is not None:
            return self.user_data["last_name"]
        else:
            return ""

    @Slot(result=str)
    def get_photo_url(self):
        return self.user_data["photo_url"]

    @Slot(result=float)
    def get_avarage_grade(self):
        return self.user_data["average_grade"]

    @Slot(result=float)
    def get_generator_percent(self):
        return self.user_data["generator_correct"] / self.user_data["generator_count"]

    # Свойства нашего qml-компонента, по которым мы можем обращаться в qml,
    # тем самым выполняя нужный код
    frame_now = Property(str, get_frame_now, set_frame_now, notify=frame_changed)
    nav_visibility = Property(bool, get_nav_visibility, set_nav_visibility,
                              notify=nav_visibility_changed)
    session_id = Property(int, get_session_id, set_session_id,
                          notify=session_id_changed)
    mode = Property(str, get_mode, set_mode,
                    notify=mode_changed)
    header = Property(str, get_header, set_header,
                      notify=header_changed)
    webpage_mode = Property(str, get_webpage_mode, set_webpage_mode, notify=webpage_mode_changed)


def check_connection(loader_manager: LoaderManager):
    """Проверяет соединение и скачивает информацию о темах"""
    try:
        response = requests.get(SERVER_URL + "session_id")
        if response.status_code == 200:
            loader_manager.frame_now = "auth.qml"
            loader_manager.session_id = response.json()["session_id"]
            loader_manager.secret_key = response.json()["secret_key"]
            loader_manager.io_thread = threading.Thread(target=check_auth, args=(loader_manager,))
            loader_manager.io_thread.start()
            topics_json = requests.get(SERVER_URL + "topics").json()
            json_to_qml_model(topics_json, "./models/TopicModel.qml")
        else:
            raise requests.exceptions.ConnectionError
    except requests.exceptions.ConnectionError:
        loader_manager.frame_now = "error.qml"


def check_auth(loader_manager: LoaderManager):
    """Проверяет авторизовался ли уже пользователь"""
    secret_data_json = {
        "session_id": loader_manager.session_id,
        "secret_key": loader_manager.secret_key
    }
    try:
        response = requests.post(SERVER_URL + "check_auth", json=secret_data_json)
        while response.status_code != 200 or response.text == "wait" or loader_manager.mode == Mode.Online:
            sleep(1)
            response = requests.post(SERVER_URL + "check_auth", json=secret_data_json)
        loader_manager.token = response.text

        loader_manager.frame_now = "topics.qml"
        tests_json = requests.get(SERVER_URL + "/tests",
                                  headers={"Authorization": loader_manager.token}).json()
        json_to_qml_model(tests_json, "./models/TestsModel.qml")
    except requests.exceptions.ConnectionError:
        loader_manager.frame_now = "error.qml"
