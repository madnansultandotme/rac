from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox, QLabel, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)

        # Appearance Section
        appearance_label = QLabel("Appearance")
        appearance_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(appearance_label)

        self.dark_theme = QCheckBox("Enable Dark Theme")
        self.dark_theme.setChecked(self.settings.value('dark_theme', 'false').lower() == 'true')
        self.dark_theme.setToolTip("Switch between light and dark themes")
        layout.addWidget(self.dark_theme)

        # AI Settings Section
        ai_label = QLabel("AI Settings")
        ai_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        layout.addWidget(ai_label)

        self.enable_memory = QCheckBox("Enable Conversation Memory")
        self.enable_memory.setChecked(self.settings.value('enable_memory', 'true').lower() == 'true')
        self.enable_memory.setToolTip("Retain conversation history for context-aware responses")
        layout.addWidget(self.enable_memory)

        tokens_layout = QHBoxLayout()
        self.tokens_label = QLabel("Max Tokens:")
        self.tokens_label.setToolTip("Maximum number of tokens in AI responses")
        tokens_layout.addWidget(self.tokens_label)
        self.max_tokens = QSpinBox()
        self.max_tokens.setMinimum(100)
        self.max_tokens.setMaximum(8192)
        self.max_tokens.setValue(int(self.settings.value('max_tokens', 500)))
        tokens_layout.addWidget(self.max_tokens)
        layout.addLayout(tokens_layout)

        context_layout = QHBoxLayout()
        self.context_label = QLabel("Context Size:")
        self.context_label.setToolTip("Size of the conversation context window")
        context_layout.addWidget(self.context_label)
        self.context_size = QSpinBox()
        self.context_size.setMinimum(512)
        self.context_size.setMaximum(8192)
        self.context_size.setSingleStep(512)
        self.context_size.setValue(int(self.settings.value('context_size', 2048)))
        context_layout.addWidget(self.context_size)
        layout.addLayout(context_layout)

        # Buttons
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def accept(self):
        self.settings.setValue('dark_theme', str(self.dark_theme.isChecked()).lower())
        self.settings.setValue('enable_memory', str(self.enable_memory.isChecked()).lower())
        self.settings.setValue('max_tokens', self.max_tokens.value())
        self.settings.setValue('context_size', self.context_size.value())
        super().accept()