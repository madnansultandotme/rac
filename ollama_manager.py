import subprocess
import time
import os
import socket
import sys
from pathlib import Path
import zipfile
from PyQt6.QtCore import QThread, pyqtSignal

DEFAULT_MODEL_NAME = "deepseek-r1:1.5b"
OLLAMA_DIR = Path.home() / ".ollama"

class CopyZipThread(QThread):
    progress_update = pyqtSignal(int)
    complete = pyqtSignal(bool, str)

    def __init__(self, zip_path, dest_dir):
        super().__init__()
        self.zip_path = zip_path 
        self.dest_dir = dest_dir

    def run(self):
        try:
            os.makedirs(self.dest_dir, exist_ok=True)
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                total_files = len(files)
                copied = 0

                for i, file in enumerate(files):
                    if '/' in file:
                        sub_path = '/'.join(file.split('/')[1:])
                        if sub_path:
                            source = zip_ref.read(file)
                            dest_path = os.path.join(self.dest_dir, sub_path)
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            if not file.endswith('/'):
                                with open(dest_path, 'wb') as f:
                                    f.write(source)
                                copied += 1
                    progress = int((i + 1) / total_files * 100)
                    self.progress_update.emit(progress)

            if copied > 0:
                self.complete.emit(True, "Model ZIP file copied successfully.")
            else:
                self.complete.emit(False, "No files were copied - check ZIP structure.")
                
        except Exception as e:
            self.complete.emit(False, f"Error copying files: {str(e)}")

class OllamaManager:
    @staticmethod
    def ensure_ollama_installed():
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @staticmethod
    def is_ollama_running():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', 11434))
            s.close()
            return result == 0
        except:
            return False

    @staticmethod
    def start_ollama_server():
        try:
            if sys.platform == "win32":
                subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            time.sleep(2)
            return OllamaManager.is_ollama_running()
        except Exception:
            return False

    @staticmethod
    def ensure_model_exists(model_name=DEFAULT_MODEL_NAME):
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return model_name in result.stdout
        except Exception:
            return False

    @staticmethod
    def pull_model(model_name=DEFAULT_MODEL_NAME):
        try:
            subprocess.Popen(["ollama", "pull", model_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False