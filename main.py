import sys
import time
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QSettings
from splash import SplashScreen
from chat_window import ChatWindow
from ollama_manager import OllamaManager

def main():
    app = QApplication(sys.argv)

    try:
        # Load settings to determine the theme for the splash screen
        settings = QSettings('RemoteAreaChatbot', 'Preferences')
        dark_theme = settings.value('dark_theme', 'false').lower() == 'true'

        # Show splash screen
        splash = SplashScreen(dark_theme)
        splash.show()
        app.processEvents()

        # Simulate initialization steps with messages
        splash.set_message("Checking Ollama installation...")
        app.processEvents()
        time.sleep(1)  # Simulate delay

        if not OllamaManager.ensure_ollama_installed():
            splash.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(
                "Ollama not found!\n\n"
                "Please install Ollama and ensure "
                "it's in your system PATH.\n\n"
                "The deepseek model can be added via a ZIP file."
            )
            msg.setWindowTitle("Missing Dependency")
            msg.exec()
            return

        splash.set_message("Starting Remote Area Chatbot...")
        app.processEvents()
        time.sleep(1)  # Simulate delay

        window = ChatWindow()
        window.show()

        splash.set_message("Loading interface...")
        app.processEvents()
        time.sleep(1)  # Simulate delay

        splash.close()

        sys.exit(app.exec())
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()