import requests

from utils import *

from PySide2.QtCore import QObject, Slot, Property


class ProfileManager(QObject):
    user_data: dict
    _token = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        user_data = requests.get(SERVER_URL + "/user_data/",
                                 headers={
                                     "Authorization": self.token}).json()

    def get_token(self):
        return self._token

    @Slot(str)
    def set_token(self, new_token):
        self._token = new_token

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
    def get_average_grade(self):
        return self.user_data["average_grade"]

    @Slot(result=float)
    def get_generator_percent(self):
        return self.user_data["generator_correct"] / self.user_data["generator_count"]

    token = Property(str, get_token, set_token)
