from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import sys

class ImageButtonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clicker")

        self.score = 0

        layout = QVBoxLayout()

        self.score_label = QLabel(f"Score: {self.score}")
        layout.addWidget(self.score_label)


        btn = QPushButton("")
        btn.setIcon(QIcon(r"C:\Users\Robocode\Documents\Projects\Python\Maker_Time\.idea\Foto\575bc383e578c1553e73bb64.png"))
        btn.setIconSize(QSize(100, 100))
        btn.setFixedSize(100, 100)

        btn.clicked.connect(self.increase_score)

        layout.addWidget(btn)
        self.setLayout(layout)

    def increase_score(self):
        self.score += 1
        self.score_label.setText(f"Score: {self.score}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageButtonWindow()
    window.show()
    sys.exit(app.exec_())
