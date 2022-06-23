import requests
from PySide2.QtCore import QObject, Slot, Signal, Property

SERVER_URL = "http://api.pank.su:25565/"


class GeneratorManager(QObject):
    answer: int

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str, result=str)
    def generate(self, token: str):
        with open("./models/generator.html", "w", encoding="utf-8") as test_file:
            test_file.write(requests.get(SERVER_URL + "generate_integral/",
                                         headers={"Authorization": token}).text)
        return "./models/generator.html"

    @Slot(float, str, result=bool)
    def check_answer(self, answer: float, token):
        return requests.post(SERVER_URL + "check_generate_integral/",
                             headers={"Authorization": token}, json={"answer": answer}).json()[
            "is_correct"]
