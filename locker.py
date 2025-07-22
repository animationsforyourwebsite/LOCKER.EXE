import sys
import os
from PyQt6.QtCore import QTimer, QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

STOP_FILE = r'C:\Users\billl\Downloads\LOCKER\stop_watchdog.txt'

class LockerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LOCKER")
        self.resize(800, 600)

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.showFullScreen()

        self.layout = QVBoxLayout(self)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL (e.g. https://example.com)")
        self.layout.addWidget(self.url_input)

        self.timer_input = QLineEdit(self)
        self.timer_input.setPlaceholderText("Enter timer in seconds")
        self.layout.addWidget(self.timer_input)

        self.start_button = QPushButton("Start Lock", self)
        self.start_button.clicked.connect(self.start_lock)
        self.layout.addWidget(self.start_button)

        self.countdown_label = QLabel("", self)
        self.layout.addWidget(self.countdown_label)

        self.webview = QWebEngineView(self)
        self.layout.addWidget(self.webview)
        self.webview.hide()

        self.webview.loadFinished.connect(self.on_load_finished)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.seconds_left = 0

    def start_lock(self):
        url = self.url_input.text().strip()
        try:
            self.seconds_left = int(self.timer_input.text())
            if self.seconds_left <= 0:
                self.countdown_label.setText("Timer must be a positive number!")
                return
        except ValueError:
            self.countdown_label.setText("Please enter a valid number for timer!")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        self.countdown_label.setText("Loading URL...")
        self.webview.load(QUrl(url))
        self.webview.show()
        self.webview.raise_()

        self.url_input.setEnabled(False)
        self.timer_input.setEnabled(False)
        self.start_button.setEnabled(False)

    def on_load_finished(self, success):
        if success:
            self.countdown_label.setText(f"Locked for {self.seconds_left} seconds")
            self.timer.start(1000)  # Start timer only after URL loads
        else:
            self.countdown_label.setText("Failed to load URL. Check your link.")
            self.url_input.setEnabled(True)
            self.timer_input.setEnabled(True)
            self.start_button.setEnabled(True)
            self.webview.hide()

    def update_countdown(self):
        if self.seconds_left > 0:
            self.countdown_label.setText(f"Locked for {self.seconds_left} seconds")
            self.seconds_left -= 1

            self.raise_()
            self.activateWindow()
            self.setFocus()

        else:
            self.timer.stop()
            # Create stop file to signal watchdog
            try:
                with open(STOP_FILE, 'w') as f:
                    f.write('stop')
            except Exception as e:
                print(f"Failed to write stop file: {e}")

            self.close()

    def closeEvent(self, event):
        if self.timer.isActive():
            event.ignore()
        else:
            event.accept()

    def keyPressEvent(self, event):
        # Block Alt+F4
        if event.key() == Qt.Key.Key_F4 and event.modifiers() & Qt.KeyboardModifier.AltModifier:
            event.accept()
            return

        # Block Ctrl+Esc
        if event.key() == Qt.Key.Key_Escape and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            event.accept()
            return

        # Block Ctrl+W
        if event.key() == Qt.Key.Key_W and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            event.accept()
            return

        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    locker = LockerApp()
    locker.show()
    sys.exit(app.exec())
