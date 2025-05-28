def get_light_theme():
    return """
        QMainWindow {
            background-color: #F5F7FA;
            font-family: Roboto, sans-serif;
        }
        #userMessage, #botMessage {
            white-space: pre-wrap;
        }
        #chatScroll {
            border: none;
            background-color: transparent;
        }
        #messageFrame {
            background: transparent;
            border: none;
            margin: 8px;
        }
        #userMessage {
            background: #26A69A;
            color: white;
            border-radius: 20px;
            padding: 12px;
            border: none;
            font-size: 18px;
        }
        #botMessage {
            background: #FFFFFF;
            color: #212121;
            border-radius: 20px;
            padding: 12px;
            border: none;
            font-size: 18px;
        }
        #inputFrame {
            background: #FFFFFF;
            border-radius: 25px;
            padding: 12px;
            margin: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        #inputField {
            border: none;
            border-radius: 20px;
            padding: 12px;
            background: #E0F2F1;
            color: #212121;
            font-size: 18px;
        }
        #inputField:focus {
            outline: none;
            box-shadow: 0 0 5px #26A69A;
        }
        #sendButton {
            background: #26A69A;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 18px;
        }
        #sendButton:hover {
            background: #00897B;
        }
        #loadingDots {
            color: #26A69A;
            font-size: 16px;
            font-weight: bold;
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        #copyButton {
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 6px 12px;
            font-size: 14px;
            margin-top: 8px;
        }
        #copyButton:hover {
            background: #45A049;
        }
        QProgressBar {
            border: 2px solid #26A69A;
            border-radius: 8px;
            text-align: center;
            background-color: #E0F2F1;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #4DB6AC);
        }
    """

def get_dark_theme():
    return """
        QMainWindow {
            background-color: #212121;
            font-family: Roboto, sans-serif;
        }
        QMenuBar {
            color: white;
        }
        QMenu {
            color: white;
            background-color: #2E2E2E;
        }
        QWidget {
            background-color: #212121;
            color: white;
        }
        #chatWindow {
            background-color: #212121;
        }
        #userMessage, #botMessage {
            white-space: pre-wrap;
        }
        #chatScroll {
            border: none;
            background-color: #212121;
        }
        #messageFrame {
            background: transparent;
            border: none;
            margin: 8px;
        }
        #userMessage {
            background: #26A69A;
            color: white;
            border-radius: 20px;
            padding: 12px;
            border: none;
            font-size: 18px;
        }
        #botMessage {
            background: #2E2E2E;
            color: white;
            border-radius: 20px;
            padding: 12px;
            border: none;
            font-size: 18px;
        }
        #inputFrame {
            background: #2E2E2E;
            border-radius: 25px;
            padding: 12px;
            margin: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        #inputField {
            border: none;
            border-radius: 20px;
            padding: 12px;
            background: #37474F;
            color: white;
            font-size: 18px;
        }
        #inputField:focus {
            outline: none;
            box-shadow: 0 0 5px #26A69A;
        }
        #sendButton {
            background: #26A69A;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 18px;
        }
        #sendButton:hover {
            background: #00897B;
        }
        #loadingDots {
            color: #26A69A;
            font-size: 16px;
            font-weight: bold;
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        #copyButton {
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 6px 12px;
            font-size: 14px;
            margin-top: 8px;
        }
        #copyButton:hover {
            background: #45A049;
        }
        QProgressBar {
            border: 2px solid #26A69A;
            border-radius: 8px;
            text-align: center;
            background-color: #37474F;
            color: white;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #26A69A, stop:1 #4DB6AC);
        }
    """