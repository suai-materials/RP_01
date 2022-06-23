from PySide2.QtCore import QObject, Slot, Signal, Property


class GeneratorManager(QObject):
    answer: int

    @Slot(result=str)
    def generate(self):

        return "generator.html"
