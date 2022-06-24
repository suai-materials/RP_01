# здесь хранятся некоторые данные и утилиты, необходимые программе
from enum import Enum

SERVER_URL = "http://api.pank.su:25565/"


class Mode(Enum):
    Offline = -1
    Online = 0


class WebPageMode(Enum):
    Topic = 0
    Test = 1
    NotShowing = 2


def json_to_qml_model(json_array: list, filename: str):
    """Преобразует json в qml модель"""
    with open(filename, "w", encoding="utf-8") as topic_model_file:
        topic_model_file.write("""import QtQuick 2.0\n
ListModel {\n""")
        for obj in json_array:
            topic_model_file.write("    ListElement {\n")
            [topic_model_file.write(f"""        {key}: {repr(value)}\n""")
             for key, value in obj.items()]
            topic_model_file.write("    }\n")
        topic_model_file.write("}")
