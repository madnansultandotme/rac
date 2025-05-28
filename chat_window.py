from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFrame, QStatusBar, QMessageBox, QFileDialog, QProgressBar, QLabel, QDialog
from PyQt6.QtGui import QKeySequence, QIcon, QShortcut
from PyQt6.QtCore import Qt, QSettings, QTimer
from chat_area import ChatArea
from ollama_manager import OllamaManager, CopyZipThread  # Added CopyZipThread import
from settings_dialog import SettingsDialog
from styles import get_light_theme, get_dark_theme
from utils import resource_path
from ollama_thread import OllamaThread
from pathlib import Path

# Define LoadingDots class within chat_window.py
class LoadingDots(QLabel):
    def __init__(self):
        super().__init__()
        self.setObjectName("loadingDots")
        self.setText("Loading")
        self.hide()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dots)
        self.dots = ""

    def start(self):
        self.show()
        self.timer.start(500)

    def stop(self):
        self.timer.stop()
        self.hide()
        self.dots = ""
        self.setText("Loading")

    def update_dots(self):
        self.dots = self.dots + "." if len(self.dots) < 3 else ""
        self.setText("Loading" + self.dots)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('RemoteAreaChatbot', 'Preferences')
        self.ollama_thread = None
        self.model_pull_thread = None
        self.current_response = ""
        self.current_bot_message = None
        self.model_name = "deepseek-r1:1.5b"
        self.conversation_history = []
        self.init_ui()
        self.check_model_availability()

    def init_ui(self):
        self.setWindowTitle("Remote Area Chatbot")
        try:
            icon_path = resource_path("images/logo.png")
            self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass
        self.setMinimumSize(600, 800)
        self.setObjectName("chatWindow")

        self.create_menu_bar()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.chat_area = ChatArea()
        layout.addWidget(self.chat_area)

        self.loading_dots = LoadingDots()  # Now defined and accessible
        layout.addWidget(self.loading_dots, alignment=Qt.AlignmentFlag.AlignCenter)

        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_frame.setFixedHeight(120)
        input_layout = QHBoxLayout(input_frame)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message (Ctrl+Enter to send)...")
        self.input_field.setMaximumHeight(100)
        self.input_field.setObjectName("inputField")

        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.toggle_send_stop)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addWidget(input_frame)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.shortcut_escape = QShortcut(QKeySequence("Escape"), self)
        self.shortcut_escape.activated.connect(self.clear_input)
        self.shortcut_send = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_send.activated.connect(self.toggle_send_stop)

        self.apply_theme()

        self.chat_area.add_message(
            "Hello! I'm your Remote Area Chatbot. How can I help you today?",
            is_user=False
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                cursor = self.input_field.textCursor()
                cursor.insertText("\n")
                event.accept()
            else:
                event.accept()
        else:
            super().keyPressEvent(event)

    def check_model_availability(self):
        try:
            if not OllamaManager.is_ollama_running():
                if not OllamaManager.start_ollama_server():
                    QMessageBox.warning(
                        self,
                        "Ollama Server Not Running",
                        "The Ollama server is not running. Please start it manually to use the Remote Area Chatbot."
                    )
                    return
            
            if not OllamaManager.ensure_model_exists(self.model_name):
                reply = QMessageBox.question(
                    self,
                    "Model Not Found",
                    f"The {self.model_name} model is not found. Would you like to provide a ZIP file or download it?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.prompt_for_zip()
                elif reply == QMessageBox.StandardButton.No:
                    self.download_model()
                else:
                    self.status_bar.showMessage(f"Model {self.model_name} not available. Chat functionality limited.", 5000)
        except Exception:
            self.status_bar.showMessage("Error checking model availability", 5000)

    def prompt_for_zip(self):
        try:
            zip_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Model ZIP File",
                "",
                "ZIP Files (*.zip)"
            )
            if zip_path:
                self.copy_zip_file(zip_path)
            else:
                self.status_bar.showMessage("No ZIP file selected.", 5000)
        except Exception:
            self.status_bar.showMessage("Error selecting ZIP file", 5000)

    def copy_zip_file(self, zip_path):
        try:
            self.loading_dots.start()
            self.status_bar.showMessage("Copying model ZIP file...")

            self.progress_bar = QProgressBar(self)
            self.progress_bar.setMaximum(100)
            self.centralWidget().layout().addWidget(self.progress_bar)

            self.copy_thread = CopyZipThread(zip_path, Path.home() / ".ollama")  # Now properly defined
            self.copy_thread.progress_update.connect(self.update_copy_progress)
            self.copy_thread.complete.connect(self.copy_complete)
            self.copy_thread.start()

            self.input_field.setEnabled(False)
        except Exception:
            self.status_bar.showMessage("Error copying ZIP file", 5000)
            self.loading_dots.stop()
            self.input_field.setEnabled(True)

    def update_copy_progress(self, progress):
        try:
            self.progress_bar.setValue(progress)
            self.status_bar.showMessage(f"Copying model ZIP file... {progress}%")
        except Exception:
            pass

    def copy_complete(self, success, message):
        try:
            self.loading_dots.stop()
            self.input_field.setEnabled(True)
            self.centralWidget().layout().removeWidget(self.progress_bar)
            self.progress_bar.deleteLater()

            if success:
                QMessageBox.information(self, "Success", "Model loaded successfully.")
                self.status_bar.showMessage("Model loaded successfully.", 5000)
                if OllamaManager.ensure_model_exists(self.model_name):
                    self.status_bar.showMessage(f"Model {self.model_name} is now available.", 5000)
                else:
                    QMessageBox.warning(
                        self,
                        "Model Verification Failed",
                        f"The model {self.model_name} was not found in the extracted files. Please ensure the ZIP contains the correct model."
                    )
            else:
                self.status_bar.showMessage("Model copy failed.", 5000)
                QMessageBox.critical(self, "Copy Failed", message)
        except Exception:
            self.status_bar.showMessage("Error completing model copy", 5000)

    def create_menu_bar(self):
        try:
            menubar = self.menuBar()
            file_menu = menubar.addMenu("File")
            settings_action = file_menu.addAction("Settings")
            settings_action.triggered.connect(self.show_settings)
            clear_action = file_menu.addAction("Clear Chat")
            clear_action.triggered.connect(self.clear_chat)
            file_menu.addSeparator()
            exit_action = file_menu.addAction("Exit")
            exit_action.triggered.connect(self.close)

            tools_menu = menubar.addMenu("Tools")
            restart_server_action = tools_menu.addAction("Restart Ollama Server")
            restart_server_action.triggered.connect(self.restart_ollama_server)
            help_menu = menubar.addMenu("Help")
            about_action = help_menu.addAction("About")
            about_action.triggered.connect(self.show_about)
        except Exception:
            pass

    def restart_ollama_server(self):
        try:
            import subprocess
            import sys
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(["killall", "ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if OllamaManager.start_ollama_server():
                self.status_bar.showMessage("Ollama server restarted successfully", 5000)
            else:
                self.status_bar.showMessage("Failed to restart Ollama server", 5000)
                QMessageBox.warning(
                    self,
                    "Server Restart Failed",
                    "Failed to restart the Ollama server. Please try starting it manually."
                )
        except Exception:
            self.status_bar.showMessage("Error restarting server", 5000)

    def show_settings(self):
        try:
            dialog = SettingsDialog(self.settings, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.apply_theme()
        except Exception:
            pass

    def show_about(self):
        try:
            QMessageBox.about(
                self,
                "About Remote Area Chatbot",
                "Remote Area Chatbot v1.0\n\nA local AI chatbot using Ollama with DeepSeek LLM."
            )
        except Exception:
            pass

    def clear_chat(self):
        try:
            for i in reversed(range(self.chat_area.chat_layout.count() - 1)):
                widget = self.chat_area.chat_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.conversation_history.clear()
        except Exception:
            pass

    def apply_theme(self):
        try:
            if self.settings.value('dark_theme', 'false').lower() == 'true':
                self.setStyleSheet(get_dark_theme())
            else:
                self.setStyleSheet(get_light_theme())
        except Exception:
            pass

    def toggle_send_stop(self):
        if self.ollama_thread and self.ollama_thread.isRunning():
            self.stop_generation()
        else:
            self.send_message()

    def stop_generation(self):
        if self.ollama_thread and self.ollama_thread.isRunning():
            self.ollama_thread.stop()
            self.ollama_thread.wait()
            self.loading_dots.stop()
            self.send_button.setText("Send")
            self.status_bar.showMessage("Generation stopped", 3000)
            self.current_bot_message = None

    def send_message(self):
        try:
            text = self.input_field.toPlainText().strip()
            if not text:
                return

            if not OllamaManager.is_ollama_running():
                reply = QMessageBox.question(
                    self,
                    "Server Not Running",
                    "The Ollama server is not running. Would you like to start it now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    if not OllamaManager.start_ollama_server():
                        QMessageBox.critical(
                            self,
                            "Server Start Failed",
                            "Failed to start the Ollama server. Please start it manually."
                        )
                        return
                else:
                    return

            self.chat_area.add_message(text, True)
            self.conversation_history.append({'role': 'user', 'content': text})
            self.input_field.clear()

            self.current_response = ""
            self.current_bot_message = self.chat_area.add_message("", False)

            self.loading_dots.start()
            self.send_button.setText("Stop")

            if self.ollama_thread and self.ollama_thread.isRunning():
                self.ollama_thread.stop()
                self.ollama_thread.wait()

            enable_memory = self.settings.value('enable_memory', 'true').lower() == 'true'
            self.ollama_thread = OllamaThread(
                prompt=text,
                model=self.model_name,
                max_tokens=int(self.settings.value('max_tokens', 500)),
                context_size=int(self.settings.value('context_size', 2048)),
                history=self.conversation_history,
                enable_memory=enable_memory
            )
                
            self.ollama_thread.chunk_received.connect(self.handle_chunk)
            self.ollama_thread.response_complete.connect(self.handle_response_complete)
            self.ollama_thread.error_occurred.connect(self.handle_error)
            self.ollama_thread.start()

            self.status_bar.showMessage("Generating response...")
        except Exception:
            self.status_bar.showMessage("Error sending message", 5000)

    def handle_chunk(self, chunk):
        try:
            self.current_response += chunk
            if self.current_bot_message:
                formatted_html, _ = self.chat_area.render_markdown_to_html(self.current_response)
                formatted_html = self.chat_area.render_math(formatted_html)
                self.current_bot_message.setText(formatted_html)
                self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        except Exception:
            pass

    def handle_response_complete(self):
        try:
            self.loading_dots.stop()
            self.send_button.setText("Send")
            
            if self.current_bot_message:
                html_output, copy_button_data = self.chat_area.render_markdown_to_html(self.current_response)
                html_output = self.chat_area.render_math(html_output)
                self.current_bot_message.setText(html_output)
                self.conversation_history.append({'role': 'assistant', 'content': self.current_response})

            self.status_bar.showMessage("Response generated successfully", 3000)
            self.current_bot_message = None
        except Exception:
            self.status_bar.showMessage("Error completing response", 5000)

    def handle_error(self, error_message):
        try:
            self.loading_dots.stop()
            self.send_button.setText("Send")
            self.chat_area.add_message(f"Error: {error_message}\n\nPlease check if the Ollama server is running. You can restart it from Tools → Restart Ollama Server", False)
            self.status_bar.showMessage("Error occurred", 3000)
            self.current_bot_message = None
        except Exception:
            self.status_bar.showMessage("Error handling response", 5000)

    def clear_input(self):
        try:
            self.input_field.clear()
        except Exception:
            pass

    def download_model(self):
        try:
            if OllamaManager.pull_model(self.model_name):
                self.status_bar.showMessage(f"Downloading {self.model_name}... Please wait.", 5000)
            else:
                self.status_bar.showMessage(f"Failed to download {self.model_name}.", 5000)
        except Exception:
            self.status_bar.showMessage("Error initiating model download", 5000)