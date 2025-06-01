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

        # Початкові налаштування автокліку
        self.priceA = 200
        self.auto_click_power = 0  # скільки кліків додаємо кожну секунду
        self.auto_click_active = False  # чи увімкнений автоклік

        # Таймер працює постійно
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_increase_score)
        self.timer.start(1000)  # 1 секунда

        # Налаштування множника
        self.multiplier_active = False
        self.multiplier_value = 1
        self.multiplier_duration = 30  # секунд
        self.multiplier_time_left = 0

        self.multiplier_timer = QTimer()
        self.multiplier_timer.timeout.connect(self.update_multiplier_timer)

        main_layout = QVBoxLayout()

        self.score_label = QLabel(f"Score: {self.score}")
        main_layout.addWidget(self.score_label)

        h_layout = QHBoxLayout()
        self.cps_label = QLabel(f"CPS: {self.auto_click_power}/s      ")
        self.X_label = QLabel(f"X: {self.X}")
        h_layout.addWidget(self.cps_label)
        h_layout.addWidget(self.X_label)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)

        # Лейбл таймера множника
        self.multiplier_label = QLabel("")
        main_layout.addWidget(self.multiplier_label)

        # Кнопка кліку
        self.btn = QPushButton("")
        self.btn.setIcon(QIcon(r"C:\Users\Robocode\Documents\Projects\Python\Maker_Time\.idea\Foto\575bc383e578c1553e73bb64.png"))
        self.btn.setIconSize(QSize(100, 100))
        self.btn.setFixedSize(100, 100)
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

        # Горизонтальний лейаут для кнопок
        button_layout = QHBoxLayout()

        # Кнопка апгрейду
        self.btnUp = QPushButton(f"UPGRADE: {self.price}")
        self.btnUp.clicked.connect(self.increase_X)
        button_layout.addWidget(self.btnUp)

        # Кнопка автокліку
        self.btnAuto = QPushButton(f"Auto : {self.priceA}")
        self.btnAuto.clicked.connect(self.buy_auto_click)
        button_layout.addWidget(self.btnAuto)

        # Кнопка множника
        self.multiplier_price = 10
        self.btnMultiplier = QPushButton(f"Multiplier x30: {self.multiplier_price}")
        self.btnMultiplier.clicked.connect(self.buy_multiplier)
        button_layout.addWidget(self.btnMultiplier)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def increase_score(self):
        self.animate_button(self.sender())
        self.score += self.X * self.multiplier_value
        self.score_label.setText(f"Score: {self.score}")

    def increase_X(self):
        if self.score >= self.price:
            self.score -= self.price
            self.X += self.X
            self.price += self.price

            self.X_label.setText(f"X: {self.X}")
            self.btnUp.setText(f"UPGRADE: {self.price}")
            self.score_label.setText(f"Score: {self.score}")
        else:
            self.show_message("Недостатньо балів для апгрейду!", "Помилка", QMessageBox.Warning)

    def animate_button(self, button):
        original_rect = button.geometry()
        smaller_rect = original_rect.adjusted(10, 10, -10, -10)  # зменшити на 10 пікселів з кожного боку

        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(100)  # швидкість анімації в мс
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
                self.auto_click_power = 1  # перша покупка дає 1 автоклік за 1 сек
            else:
                self.auto_click_power *= 2  # подвоюємо силу автокліку

            self.priceA *= 2
            self.btnAuto.setText(f"Auto : {self.priceA}")
            self.cps_label.setText(f"CPS: {self.auto_click_power}/s      ")
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
            self.multiplier_timer.start(1000)  # кожну секунду

            self.btnMultiplier.setEnabled(False)
            self.show_message("Множник x30 активовано на 30 секунд!", "Успіх", QMessageBox.Information)
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
            self.show_message("Множник завершився.", "Інформація", QMessageBox.Information)
        else:
            self.multiplier_label.setText(f"Multiplier active: x{self.multiplier_value} - {self.multiplier_time_left} s left")

    def auto_increase_score(self):
        if self.auto_click_active:
            self.score += self.auto_click_power * self.multiplier_value
            self.score_label.setText(f"Score: {self.score}")

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
