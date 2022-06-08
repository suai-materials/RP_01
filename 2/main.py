import os
from shutil import copy2
# Перемещаем файл из первой задачи на рабочий стол
os.replace(r"..\1\TASK_1_PANKOV.txt", os.path.expanduser("~") + r"\Desktop\TASK_1_PANKOV.txt")
# Для большего удобства меняем текущий каталог
os.chdir(os.path.expanduser("~") + r"\Desktop")
# Создание папки
os.mkdir("MY_NEW_DIR")
# Копирование файла с нужным нам названием
copy2("TASK_1_PANKOV.txt", r"MY_NEW_DIR\TASK_1_ NEW_PANKOV.txt")
# Меняем директорию для показа что мы удаляем файл из род. каталога
os.chdir("MY_NEW_DIR")
# Удаляем файл из род. каталога
os.remove(r"..\TASK_1_PANKOV.txt")
# Выводим путь для необходимого файла
print(os.path.abspath("TASK_1_ NEW_NAME.txt"))