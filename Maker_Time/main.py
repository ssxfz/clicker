from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer, QPropertyAnimation, QEasingCurve
import sys


class ImageButtonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clicker")
        with open("Pengi.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.score = 0
        self.X = 1
        self.price = 10

        self.upgrade_level = 1
        self.auto_click_level = 0
        self.priceA = 200
        self.auto_click_power = 0
        self.auto_click_active = False

        self.multiplier_active = False
        self.multiplier_value = 1
        self.multiplier_duration = 5
        self.multiplier_time_left = 0

        self.multiplier_price = 10

        self.current_icon_level = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_increase_score)
        self.timer.start(1000)

        self.multiplier_timer = QTimer()
        self.multiplier_timer.timeout.connect(self.update_multiplier_timer)

        main_layout = QVBoxLayout()

        # 👉 топовий рядок: Score, CPS, X в одному рядку
        top_layout = QHBoxLayout()

        self.score_label = QLabel(f"Score: {self.score}")
        self.cps_label = QLabel(f"CPS: {self.auto_click_power}/s")
        self.X_label = QLabel(f"X: {self.X}")

        top_layout.addWidget(self.score_label)
        top_layout.addSpacing(20)
        top_layout.addWidget(self.cps_label)
        top_layout.addSpacing(20)
        top_layout.addWidget(self.X_label)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        self.multiplier_label = QLabel("")
        main_layout.addWidget(self.multiplier_label)

        self.btn = QPushButton("")
        self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64.png"))
        self.btn.setIconSize(QSize(200, 200))
        self.btn.setFixedSize(200, 200)

        self.btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.btn.clicked.connect(self.increase_score)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.btn)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)

        button_layout = QHBoxLayout()

        self.btnUp = QPushButton(f"UPGRADE {self.upgrade_level}lvl: {self.price}")
        self.btnUp.clicked.connect(self.increase_X)
        button_layout.addWidget(self.btnUp)

        self.btnAuto = QPushButton(f"Auto {self.auto_click_level}lvl: {self.priceA}")
        self.btnAuto.clicked.connect(self.buy_auto_click)
        button_layout.addWidget(self.btnAuto)

        self.btnMultiplier = QPushButton(f"Multiplier x30: {self.multiplier_price}")
        self.btnMultiplier.clicked.connect(self.buy_multiplier)
        button_layout.addWidget(self.btnMultiplier)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.update_button_icon()

    def increase_score(self):
        self.animate_button(self.sender())
        self.score += self.X * self.multiplier_value
        self.score_label.setText(f"Score: {self.score}")
        self.update_button_icon()

    def update_button_icon(self):
        if self.score >= 10000 and self.current_icon_level < 4:
            self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64sira.png"))
            self.current_icon_level = 4
        elif self.score >= 5000 and self.current_icon_level < 3:
            self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64gold.png"))
            self.current_icon_level = 3
        elif self.score >= 2500 and self.current_icon_level < 2:
            self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64red.png"))
            self.current_icon_level = 2
        elif self.score >= 1000 and self.current_icon_level < 1:
            self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64sir.png"))
            self.current_icon_level = 1

    def increase_X(self):
        if self.score >= self.price:
            self.score -= self.price
            self.X += self.X
            self.price += self.price
            self.upgrade_level += 1
            self.X_label.setText(f"X: {self.X}")
            self.btnUp.setText(f"UPGRADE {self.upgrade_level}lvl: {self.price}")
            self.score_label.setText(f"Score: {self.score}")
        else:
            self.show_message("Недостатньо балів для апгрейду!", "Помилка", QMessageBox.Warning)

    def animate_button(self, button):
        original_rect = button.geometry()
        smaller_rect = original_rect.adjusted(10, 10, -10, -10)
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(original_rect)
        self.anim.setKeyValueAt(0.5, smaller_rect)
        self.anim.setEndValue(original_rect)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()

    def buy_auto_click(self):
        if self.score >= self.priceA:
            self.score -= self.priceA
            self.score_label.setText(f"Score: {self.score}")
            if not self.auto_click_active:
                self.auto_click_active = True
                self.auto_click_power = 1
            else:
                self.auto_click_power *= 2
            self.priceA *= 2
            self.auto_click_level += 1
            self.btnAuto.setText(f"Auto {self.auto_click_level}lvl: {self.priceA}")
            self.cps_label.setText(f"CPS: {self.auto_click_power}/s")
        else:
            self.show_message("Недостатньо балів для покупки автокліку!", "Помилка", QMessageBox.Warning)

    def buy_multiplier(self):
        if self.score >= self.multiplier_price and not self.multiplier_active:
            self.score -= self.multiplier_price
            self.score_label.setText(f"Score: {self.score}")
            self.multiplier_active = True
            self.multiplier_value = 30
            self.multiplier_time_left = self.multiplier_duration
            self.multiplier_label.setText(f"Multiplier active: x{self.multiplier_value} - {self.multiplier_time_left} s left")
            self.multiplier_timer.start(1000)
            self.btn.setIcon(QIcon(r"very_angry_penguin.webp"))
            self.btnMultiplier.setEnabled(False)
        elif self.multiplier_active:
            self.show_message("Множник вже активний!", "Інформація", QMessageBox.Warning)
        else:
            self.show_message("Недостатньо балів для покупки множника!", "Помилка", QMessageBox.Warning)

    def update_multiplier_timer(self):
        self.multiplier_time_left -= 1
        if self.multiplier_time_left <= 0:
            self.multiplier_active = False
            self.multiplier_value = 1
            self.multiplier_label.setText("")
            self.multiplier_timer.stop()
            self.btnMultiplier.setEnabled(True)
            self.update_button_icon()
            self.show_message("Множник завершився.", "Інформація", QMessageBox.Information)
            self.btn.setIcon(QIcon(r"Foto\575bc383e578c1553e73bb64.png"))
        else:
            self.multiplier_label.setText(f"Multiplier active: x{self.multiplier_value} - {self.multiplier_time_left} s left")

    def auto_increase_score(self):
        if self.auto_click_active:
            self.score += self.auto_click_power * self.multiplier_value
            self.score_label.setText(f"Score: {self.score}")
            self.update_button_icon()

    def show_message(self, text, title, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageButtonWindow()
    window.show()
    sys.exit(app.exec_())
