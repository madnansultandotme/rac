from PyQt6.QtWidgets import QSplashScreen, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from utils import resource_path

LOGO_PATH = resource_path("images/logo.png")

class SplashScreen(QSplashScreen):
    def __init__(self, dark_theme=False):
        pixmap = QPixmap(400, 300)
        super().__init__(pixmap)
        self.setPixmap(pixmap)

        widget = QWidget(self)
        widget.setGeometry(0, 0, 400, 300)

        main_layout = QVBoxLayout(widget)

        # Product Name
        product_name = QLabel("Remote Area Chatbot")
        product_name.setObjectName("productName")
        product_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(product_name)

        # Product Description
        description = QLabel("Interactive Response Assistant\nPowered by DeepSeek LLM\n\nDesigned & Developed by Aqsa Abu Bakar")
        description.setObjectName("description")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description)

        # Middle layout for logo and copyright
        middle_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap(LOGO_PATH).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        except Exception:
            logo_label.setText("LOGO")
        logo_label.setFixedSize(100, 100)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        middle_layout.addWidget(logo_label)

        # Copyright Notice
        copyright_label = QLabel("© 2025 AITeC")
        copyright_label.setObjectName("copyright")
        middle_layout.addWidget(copyright_label)
        middle_layout.addStretch()

        main_layout.addLayout(middle_layout)

        # Initializing Message
        self.initializing_label = QLabel("Initializing...")
        self.initializing_label.setObjectName("initializing")
        self.initializing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.initializing_label)

        main_layout.addStretch()

        self.apply_theme(dark_theme)

    def apply_theme(self, dark_theme):
        if dark_theme:
            self.setStyleSheet("""
                QWidget {
                    background-color: #212121;
                    color: white;
                    font-family: Roboto, sans-serif;
                }
                #productName {
                    font-size: 26px;
                    font-weight: bold;
                    transition: opacity 1s ease-in;
                }
                #description {
                    font-size: 14px;
                    opacity: 0.9;
                }
                #copyright {
                    font-size: 12px;
                    opacity: 0.7;
                }
                #initializing {
                    font-size: 14px;
                    font-style: italic;
                    transition: opacity 0.5s ease-in;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #F5F7FA;
                    color: #212121;
                    font-family: Roboto, sans-serif;
                }
                #productName {
                    font-size: 26px;
                    font-weight: bold;
                    transition: opacity 1s ease-in;
                }
                #description {
                    font-size: 14px;
                    opacity: 0.9;
                }
                #copyright {
                    font-size: 12px;
                    opacity: 0.7;
                }
                #initializing {
                    font-size: 14px;
                    font-style: italic;
                    transition: opacity 0.5s ease-in;
                }
            """)

    def set_message(self, message):
        self.initializing_label.setText(message)