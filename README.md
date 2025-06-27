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
