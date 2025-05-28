from PyQt6.QtCore import QThread, pyqtSignal
from ollama_manager import OllamaManager, DEFAULT_MODEL_NAME

class OllamaThread(QThread):
    chunk_received = pyqtSignal(str)
    response_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, prompt, model=DEFAULT_MODEL_NAME, max_tokens=500, context_size=2048, history=None, enable_memory=True):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.context_size = context_size
        self.history = history if history is not None else []
        self.enable_memory = enable_memory
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        try:
            import ollama

            if not OllamaManager.is_ollama_running():
                if not OllamaManager.start_ollama_server():
                    self.error_occurred.emit("Ollama server is not running. Please start the Ollama server manually.")
                    return

            if self.enable_memory:
                messages = self.history + [{'role': 'user', 'content': self.prompt}]
            else:
                messages = [{'role': 'user', 'content': self.prompt}]

            try:
                response_stream = ollama.chat(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    options={
                        'num_predict': self.max_tokens,
                        'num_ctx': self.context_size
                    }
                )

                for chunk in response_stream:
                    if self._stop_requested:
                        break
                    if 'message' in chunk and 'content' in chunk['message']:
                        chunk_content = chunk['message']['content']
                        self.chunk_received.emit(chunk_content)

                if not self._stop_requested:
                    self.response_complete.emit()
            except Exception:
                self.error_occurred.emit("Error generating response: Connection to Ollama server failed. Please ensure it's running.")

        except Exception:
            self.error_occurred.emit("Unexpected error: Unable to connect to Ollama server.")