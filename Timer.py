import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout

class Timer(QDialog):
    def __init__(self, duration, parent=None):
        super(Timer, self).__init__(parent)

        self.duration = duration
        self.remaining_time = duration

        self.init_ui()
        self.init_timer()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel(f'Time remaining: {self.remaining_time} seconds', self)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.setWindowTitle('Timer Dialog')

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        self.remaining_time -= 1
        self.label.setText(f'Time remaining: {self.remaining_time} seconds')

        if self.remaining_time <= 0:
            self.timer.stop()
            self.accept()

def main():
    app = QApplication(sys.argv)
    dialog = Timer(duration=10)  # 10-second timer
    dialog.exec_()

if __name__ == '__main__':
    main()

