import sys
import importlib
import time
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class AstraUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.S.T.R.A. Interface")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        # Main layout
        main_layout = QVBoxLayout()
        
        # Top layout for CPU and system status
        top_layout = QHBoxLayout()
        
        # CPU usage display (top left) - Made larger
        self.cpu_label = QLabel("CPU Usage: 0%", self)
        self.cpu_label.setAlignment(Qt.AlignLeft)
        self.cpu_label.setStyleSheet("color: #00FFFF;")
        self.cpu_label.setFont(QFont('Arial', 32))  # Increased font size
        
        # System status (top right) - Made larger
        self.system_label = QLabel("System Online", self)
        self.system_label.setAlignment(Qt.AlignRight)
        self.system_label.setStyleSheet("color: #00FFFF;")
        self.system_label.setFont(QFont('Arial', 32))  # Increased font size
        
        top_layout.addWidget(self.cpu_label)
        top_layout.addWidget(self.system_label)
        main_layout.addLayout(top_layout)
        
        # A.S.T.R.A. label in center - Made larger
        self.circle_label = QLabel("A.S.T.R.A", self)
        self.circle_label.setAlignment(Qt.AlignCenter)
        self.circle_label.setFont(QFont('Arial', 120, QFont.Bold))  # Increased font size
        self.circle_label.setStyleSheet("color: #00FFFF; border: 4px solid #00FFFF; border-radius: 120px; padding: 30px;")  # Increased size
        main_layout.addWidget(self.circle_label, 1, Qt.AlignCenter)
        
        # Bottom layout for buttons
        bottom_layout = QHBoxLayout()
        
        # H.A.N.D.S button (bottom left) - Made larger
        self.hands_button = QPushButton("H.A.N.D.S", self)
        self.hands_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00FFFF;
                border: 3px solid #00FFFF;
                border-radius: 15px;
                font-size: 28px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 50);
            }
        """)
        self.hands_button.setFixedSize(200, 70)  # Increased button size
        
        self.hands_button.clicked.connect(self.launch_hands)
        
        # I.R.I.S button (bottom right) - Made larger
        self.iris_button = QPushButton("I.R.I.S", self)
        self.iris_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00FFFF;
                border: 3px solid #00FFFF;
                border-radius: 15px;
                font-size: 28px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 50);
            }
        """)
        self.iris_button.setFixedSize(200, 70)  # Increased button size
        self.iris_button.clicked.connect(self.launch_iris)
        
        bottom_layout.addWidget(self.hands_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.iris_button, alignment=Qt.AlignRight)
        main_layout.addLayout(bottom_layout)
        
        # Update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        
        self.setLayout(main_layout)

    def update_info(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

    def launch_hands(self):
        try:
            # Close the interface first
            self.close()
            # Then try to import the module
            importlib.import_module("hands")
        except ImportError:
            print("H.A.N.D.S module not found")
            
    def launch_iris(self):
        try:
            # Close the interface first
            self.close()
            # Then try to import the module
            importlib.import_module("iris")
        except ImportError:
            print("I.R.I.S module not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AstraUI()
    window.show()
    sys.exit(app.exec_())
