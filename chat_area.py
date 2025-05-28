import markdown
import re
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QApplication
from PyQt6.QtGui import QPixmap, QClipboard
from PyQt6.QtCore import Qt
from utils import resource_path

USER_ICON_PATH = resource_path("images/user_icon.png")
BOT_ICON_PATH = resource_path("images/bot_icon.png")

class ChatArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setObjectName("chatScroll")

        container = QWidget()
        self.chat_layout = QVBoxLayout(container)
        self.chat_layout.addStretch()
        self.setWidget(container)

    def add_message(self, text, is_user=False):
        frame = QFrame()
        frame.setObjectName("messageFrame")
        layout = QHBoxLayout(frame)

        icon_label = QLabel()
        icon_path = USER_ICON_PATH if is_user else BOT_ICON_PATH
        pixmap = QPixmap(icon_path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(32, 32)

        message_container = QWidget()
        message_layout = QVBoxLayout(message_container)

        message = QLabel()
        message.setWordWrap(True)
        message.setObjectName("userMessage" if is_user else "botMessage")
        message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        formatted_html, copy_button_data = self.render_markdown_to_html(text)
        formatted_html = self.render_math(formatted_html)
        message.setText(formatted_html)

        message_layout.addWidget(message)

        if not is_user and copy_button_data:
            copy_button = QPushButton("Copy")
            copy_button.setObjectName("copyButton")
            copy_button.clicked.connect(lambda checked, d=copy_button_data[-1]: self.copy_to_clipboard(d))
            message_layout.addWidget(copy_button)

        message_layout.addStretch()
        message_container.setLayout(message_layout)

        if is_user:
            layout.addStretch()
            layout.addWidget(message_container)
            layout.addWidget(icon_label)
        else:
            layout.addWidget(icon_label)
            layout.addWidget(message_container)
            layout.addStretch()

        self.chat_layout.insertWidget(self.chat_layout.count() - 1, frame)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        return message

    def render_markdown_to_html(self, markdown_text):
        html_output = ""
        copy_button_data = []
        in_think = False
        current_pos = 0
        think_start = -1
        think_end = -1

        try:
            think_match = re.search(r'<think>', markdown_text)
            think_end_match = re.search(r'</think>', markdown_text)
            if think_match and think_end_match:
                think_start = think_match.start()
                think_end = think_end_match.end()

            i = 0
            while i < len(markdown_text):
                if think_start != -1 and i == think_start:
                    if current_pos < think_start:
                        chunk = markdown_text[current_pos:think_start].strip()
                        if chunk:
                            html_output += markdown.markdown(chunk, extensions=['fenced_code', 'tables'])
                    in_think = True
                    current_pos = think_start + len('<think>')
                    i = current_pos
                    continue

                if think_end != -1 and i == think_end - len('</think>'):
                    think_content = markdown_text[current_pos:think_end - len('</think>')].strip()
                    if think_content:
                        html_output += f'<blockquote style="border-left: 4px solid #B0BEC5; padding-left: 12px; color: #546E7A; margin: 10px 0;">{markdown.markdown(think_content, extensions=["fenced_code", "tables"])}</blockquote>'
                    in_think = False
                    current_pos = think_end
                    i = think_end
                    continue

                code_match = re.search(r'```[\s\S]*?```', markdown_text[i:])
                if code_match:
                    code_start = i + code_match.start()
                    code_end = i + code_match.end()

                    if current_pos < code_start:
                        chunk = markdown_text[current_pos:code_start].strip()
                        if chunk:
                            if in_think:
                                html_output += f'<blockquote style="border-left: 4px solid #B0BEC5; padding-left: 12px; color: #546E7A; margin: 10px 0;">{markdown.markdown(chunk, extensions=["fenced_code", "tables"])}</blockquote>'
                            else:
                                html_output += markdown.markdown(chunk, extensions=['fenced_code', 'tables'])

                    code_block = markdown_text[code_start:code_end]
                    html_code = markdown.markdown(code_block, extensions=['fenced_code', 'tables'])
                    html_output += html_code

                    current_pos = code_end
                    i = code_end
                    continue

                i += 1

            if current_pos < len(markdown_text):
                remaining_text = markdown_text[current_pos:].strip()
                if remaining_text:
                    html_output += markdown.markdown(remaining_text, extensions=['fenced_code', 'tables'])

            return html_output, copy_button_data

        except Exception:
            return f"<p>{markdown_text}</p>", []

    def render_math(self, html_text):
        html_text = html_text.strip()

        def process_sqrt(match):
            expr = match.group(1) if match.group(1) else match.group(2)
            rendered_expr = self.render_math(expr)
            return f'√(<span style="text-decoration: overline;">{rendered_expr}</span>)'

        html_text = re.sub(r'\\sqrt\{([^}]*)\}', process_sqrt, html_text)
        html_text = re.sub(r'\\sqrt\s+([^\s\\]+)', process_sqrt, html_text)

        def process_fraction(match):
            num = match.group(1)
            denom = match.group(2)
            rendered_num = self.render_math(num)
            rendered_denom = self.render_math(denom)
            return f'<span style="display: inline-block; white-space: nowrap;"><sup>{rendered_num}</sup>⁄<sub>{rendered_denom}</sub></span>'

        html_text = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', process_fraction, html_text)
        html_text = re.sub(r'\\dfrac\{([^}]*)\}\{([^}]*)\}', process_fraction, html_text)

        def process_boxed(match):
            expr = match.group(1)
            rendered_expr = self.render_math(expr)
            return f'<span style="border: 1px solid #B0BEC5; padding: 6px; display: inline-block; white-space: nowrap;">{rendered_expr}</span>'

        html_text = re.sub(r'\\boxed\{([^}]*)\}', process_boxed, html_text)

        replacements = {
            r'\times': '×',
            r'\quad': ' ',
            r'\approx': '≈',
            r'\text{': '<span style="font-style: italic;">',
            r'}': '</span>'
        }
        for latex, html in replacements.items():
            html_text = html_text.replace(latex, html)

        def process_inline_math(match):
            expr = match.group(1)
            rendered_expr = self.render_math(expr)
            return f'<span style="font-family: monospace; white-space: nowrap;">{rendered_expr}</span>'

        html_text = re.sub(r'\\\((.*?)\\\)', process_inline_math, html_text)

        def process_display_math(match):
            expr = match.group(1)
            rendered_expr = self.render_math(expr)
            return f'<span style="font-family: monospace; white-space: nowrap;">{rendered_expr}</span>'

        html_text = re.sub(r'\\\[(.*?)\\\]', process_display_math, html_text)

        def process_paren_display_math(match):
            expr = match.group(1).strip()
            rendered_expr = self.render_math(expr)
            return f'<span style="font-family: monospace; white-space: nowrap;">({rendered_expr})</span>'

        html_text = re.sub(r'\(\s*([^()]+)\s*\)', process_paren_display_math, html_text)

        return html_text

    def copy_to_clipboard(self, html_text):
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(html_text)
        except Exception:
            pass