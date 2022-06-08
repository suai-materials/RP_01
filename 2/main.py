import os
from sys import exit
from shutil import copy2

# Перемещаем файл из первой задачи на рабочий стол
try:
    os.replace(r"..\1\TASK_1_PANKOV.txt", os.path.expanduser("~") + r"\Desktop\TASK_1_PANKOV.txt")
except FileNotFoundError:
    exit("Файл не найден, перезапустите программу.")
# Для большего удобства меняем текущий каталог на рабочий код
os.chdir(os.path.expanduser("~") + r"\Desktop")
# Вывод содержимого рабочего стола
print("Файл перемещён на рабочий стол" +
      f", новое расположение файла: {os.path.abspath('TASK_1_PANKOV.txt')}\n")
print("Содержимое рабочего стола:")
[print(item) for item in os.listdir()]
# Создание папки, если папка была создана, то ошибки не будет
os.makedirs("MY_NEW_DIR", exist_ok=True)
# Копирование файла с нужным нам названием
copy2("TASK_1_PANKOV.txt", r"MY_NEW_DIR\TASK_1_ NEW_PANKOV.txt")
print(
    "\nСоздана копия. Путь до копии: " + os.path.abspath('MY_NEW_DIR\TASK_1_ NEW_PANKOV.txt') + "\n")
# Меняем директорию для показа что мы удаляем файл из род. каталога
os.chdir("MY_NEW_DIR")
# Удаляем файл из род. каталога
os.remove(r"..\TASK_1_PANKOV.txt")
# Выводим путь для необходимого файла
print("Файл копии на рабочем столе удалён.\n")
print("Содержимое рабочего стола:")
[print(item) for item in os.listdir("..")]
print("\nПуть до расположения файла:", end="")
print(os.path.abspath("TASK_1_ NEW_PANKOV.txt"))
