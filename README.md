
# PythonRAT for macOS

> ⚠️ **Disclaimer:**  
> This project is for **educational and research purposes only**. Unauthorized use to access or control systems without explicit permission is **illegal** and **unethical**. The author is not responsible for any misuse or damage caused by this software. Ensure compliance with all applicable laws and regulations.

## 🧠 About

**PythonRAT** is an educational Remote Access Tool (RAT) written in Python, specifically designed for learning and research on macOS systems. It allows remote control via Telegram commands and supports features like screen capturing, webcam access, file management, and system information retrieval.

## ✨ Features

- 📸 **Screen Capture**: Capture the desktop (excluding menu bar and dock on macOS).
- 🎥 **Webcam Access**: Take webcam images with brightness/exposure optimizations.
- 💻 **System Information**: Fetch OS, CPU, and user info.
- 📁 **File Management**: Navigate directories, list/upload files, and encrypt/decrypt content.
- 🖥️ **Remote Shell**: Execute shell commands.
- 📡 **WiFi Password Retrieval**: Extract saved WiFi passwords (macOS and Windows).
- 📋 **Clipboard Access**: Read the system clipboard.
- 🔒 **System Control**: Lock the screen (macOS and Windows).
- 🗣️ **Text-to-Speech**: Convert text to speech output.

## 🛠️ Prerequisites

- **Python** 3.12 or higher
- A **Telegram Bot Token** (get one from [@BotFather](https://t.me/BotFather))
- OS: Tested on **macOS**, partially compatible with **Windows**
- **Dependencies**:
  ```bash
  pip install mss opencv-python numpy pyttsx3 telebot pyAesCrypt secure_delete pyperclip Pillow
  ```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/annapurnageeks/RAT-for-MAC.git
cd RAT-for-MAC
```

### 2. Install Dependencies
You can either install dependencies manually:
```bash
pip install mss opencv-python numpy pyttsx3 telebot pyAesCrypt secure_delete pyperclip Pillow
```

Or use a `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configure the Bot Token
Open `PythonRAT.py` and replace:
```python
TOKEN = 'your_bot_token_here'
```
with your actual bot token from BotFather.

## ▶️ Running the Script

To start the bot:
```bash
python PythonRAT.py
```

Now you can interact via Telegram with commands like `/start`, `/screen`, `/webcam`, etc.

## 📦 Creating a Standalone Executable (Optional)

### Install PyInstaller
```bash
pip install pyinstaller
```

### Build the Executable (macOS example)
```bash
python -m PyInstaller --onefile --add-data "PythonRAT.py:." --add-data "$(python -c 'import numpy; print(numpy.__path__[0])'):numpy" --add-data "$(python -c 'import cv2; print(cv2.__path__[0])'):cv2" --hidden-import=mss --hidden-import=cv2 --hidden-import=numpy --hidden-import=numpy._core --hidden-import=numpy._core._exceptions --hidden-import=pyttsx3 --hidden-import=telebot --hidden-import=pyAesCrypt --hidden-import=secure_delete --hidden-import=pyperclip --hidden-import=xml.etree.ElementTree --hidden-import=PIL --name PythonRAT PythonRAT.py
```

### Locate and Run
```bash
chmod +x dist/PythonRAT
./dist/PythonRAT
```

> 💡 Windows users: Replace colons (`:`) with semicolons (`;`) in `--add-data`.

## 💬 Telegram Commands

| Command              | Description                                    |
|----------------------|------------------------------------------------|
| `/start`             | Initialize the bot                             |
| `/help`              | Show available commands                        |
| `/screen`            | Capture a screenshot                           |
| `/webcam`            | Capture a webcam image                         |
| `/sys`               | Get system information                         |
| `/ip`                | Get public IP address                          |
| `/cd [folder]`       | Change directory                               |
| `/ls`                | List files in current directory                |
| `/upload [path]`     | Upload a file                                  |
| `/crypt [path]`      | Encrypt files in folder                        |
| `/decrypt [path]`    | Decrypt files in folder                        |
| `/lock`              | Lock the screen                                |
| `/clipboard`         | Show clipboard contents                        |
| `/shell`             | Enter remote shell mode                        |
| `/wifi`              | Retrieve WiFi passwords                        |
| `/speech [text]`     | Convert text to speech                         |

## 🧪 Logs & Debugging

macOS:
```bash
cat ~/Library/Logs/PythonRAT.log
```

Windows:
```cmd
type %USERPROFILE%\PythonRAT.log
```

Enable detailed logs in `PythonRAT.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Check dependencies or add `--hidden-import` to PyInstaller |
| Permissions | On macOS, grant **Screen Recording** and **Camera** permissions in System Settings |
| Dark Webcam Feed | Tweak OpenCV brightness/exposure/gain settings |
| Screen Capture Issues | Adjust `mss` capture region in `send_screen()` function |

macOS permission reset:
```bash
sudo tccutil reset ScreenCapture
sudo tccutil reset Camera
```

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit and push:
   ```bash
   git commit -m "Add YourFeature"
   git push origin feature/YourFeature
   ```
4. Open a pull request!

> 🚫 **Important:** Do **NOT** upload your compiled executable or your Telegram bot token to GitHub.

---

## ✅ Final Notes

- ✅ Educational and ethical use only
- ✅ macOS-optimized; partially works on Windows
- ✅ Use in secure and controlled environments

For feedback, support, or enhancements, feel free to open an issue or pull request.

---
