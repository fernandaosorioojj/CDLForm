from PyQt5.QtWidgets import QFrame


class CardFrame(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setProperty("card", "true")

