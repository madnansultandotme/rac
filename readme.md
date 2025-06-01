# Remote Area Chatbot

## Overview
Remote Area Chatbot is a desktop application designed to provide an interactive chat experience using a local AI model powered by Ollama and the DeepSeek LLM (deepseek-r1:1.5b). This application is ideal for users in remote areas with limited internet access, as it runs entirely offline after initial setup. It features a modern, user-friendly interface with soft colors, dark/light theme support, and accessibility enhancements.

The project was developed by Aqsa Abu Bakar and is maintained by the AITeC team. The application was last updated on May 29, 2025.
## Slides

[Click here to view the slides](https://pern-my.sharepoint.com/:f:/g/personal/04072113023_student_qau_edu_pk/EkL7CKqaiJhGnewNlW9obFMBUvgLuW48TfcN5dvHQOtm_g?e=JGPl30)


## Features

- **Offline Chat**: Communicate with the DeepSeek AI model without an internet connection (after model download).
- **Modern UI/UX**: Soft color palette (teal and off-white), rounded edges, and smooth animations for a pleasant user experience.
- **Theme Support**: Toggle between light and dark themes.
- **Conversation Memory**: Retains chat history for context-aware responses (configurable).
- **Markdown Support**: Renders markdown in chat messages, including code blocks and tables.
- **Math Rendering**: Supports basic LaTeX math expressions in responses.
- **Model Management**: Download or load the DeepSeek model via ZIP file.
- **Accessibility**: Keyboard shortcuts (e.g., Ctrl+Enter to send messages) and visible focus states.
- **Settings**: Customize max tokens, context size, and memory settings.

## Screenshots
*(Screenshots of the application can be added here, e.g., splash screen, chat window, settings dialog.)*

## Prerequisites

- **Operating System**: Windows, macOS, or Linux.
- **Python**: Version 3.8 or higher.
- **Ollama**: Required for running the DeepSeek LLM locally.
- **Disk Space**: At least 5GB for the DeepSeek model (deepseek-r1:1.5b).

## Installation

### 1. Clone or Download the Project
Download the project files and extract them to a directory (e.g., `remote_area_chatbot/`).

### 2. Set Up a Python Environment
It's recommended to use a virtual environment to avoid dependency conflicts:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies
Install the required Python libraries using pip:
```bash
pip install PyQt6 markdown ollama
```

### 4. Install Ollama
Ollama is required to run the AI model locally. Follow the instructions for your operating system:

**Windows**:
```
Download the Ollama installer from the official Ollama website.
Run the installer and follow the prompts.
Verify installation: ollama --version
```

**macOS**:
```bash
# Install Ollama using Homebrew:
brew install ollama

# Start the Ollama server:
ollama serve

# Verify installation:
ollama --version
```

**Linux**:
```bash
# Install Ollama:
curl -fsSL https://ollama.com/install.sh | sh

# Start the Ollama server:
ollama serve

# Verify installation:
ollama --version
```

### 5. Download the DeepSeek Model
The application uses the deepseek-r1:1.5b model. If it's not already downloaded, the application will prompt you to download it or provide a ZIP file. To manually download the model:
```bash
ollama pull deepseek-r1:1.5b
```
Ensure the Ollama server is running when executing this command.

### 6. Set Up the Images Folder
The application requires an `images/` folder in the project directory containing the following files:
- `user_icon.png`
- `bot_icon.png`
- `logo.png`

These images have been generated and provided for the project. Ensure they are placed in the `images/` subdirectory.

## Project Structure
```
remote_area_chatbot/
├── images/
│   ├── user_icon.png
│   ├── bot_icon.png
│   └── logo.png
├── main.py
├── splash.py
├── chat_window.py
├── chat_area.py
├── ollama_manager.py
├── settings_dialog.py
├── styles.py
├── utils.py
├── ollama_thread.py
└── README.md
```

## Usage

1. Ensure the Ollama server is running:
```bash
ollama serve
```

2. Navigate to the project directory and run the application:
```bash
python main.py
```

3. The splash screen will appear, followed by the main chat window.
4. Type your message in the input field and press Ctrl+Enter or click the "Send" button to chat with the bot.
5. Use the menu bar to access settings, clear the chat, or restart the Ollama server if needed.

## Configuration

- **Settings**: Access via the "File > Settings" menu to toggle the dark theme, enable/disable conversation memory, and adjust max tokens and context size.
- **Themes**: The application uses a soft teal (#26A69A) and off-white (#F5F7FA) for the light theme, and a dark gray (#212121) for the dark theme.
- **Fonts**: The application uses the Roboto font. Install it from Google Fonts if not already on your system.

## Troubleshooting

- **Ollama Server Not Running**: If the server fails to start, ensure Ollama is installed and in your system PATH. Start it manually with `ollama serve`.
- **Model Not Found**: If the deepseek-r1:1.5b model is missing, download it using `ollama pull deepseek-r1:1.5b` or provide a ZIP file when prompted.
- **Dependency Issues**: Ensure all Python libraries are installed correctly. Use a virtual environment to avoid conflicts.
- **UI Issues**: If the UI doesn't render correctly, ensure PyQt6 is installed and your system supports Qt applications.

## Contributing
Contributions are welcome! Please fork the project, make your changes, and submit a pull request with a detailed description of your updates.

---

**Powered By**: Ollama, DeepSeek LLM
