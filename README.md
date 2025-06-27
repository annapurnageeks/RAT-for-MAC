PythonRAT
PythonRAT is an educational Remote Access Tool (RAT) written in Python for learning and research purposes. It enables remote control of a system via Telegram commands, supporting features like screen capture, webcam access, file management, and system information retrieval. This project is designed for ethical use in controlled environments (e.g., testing or learning about remote administration) and should not be used for unauthorized access or malicious activities.
⚠️ Disclaimer: This project is for educational and research purposes only. Unauthorized use to access or control systems without explicit permission is illegal and unethical. The author is not responsible for any misuse or damage caused by this software. Ensure compliance with all applicable laws and regulations.
Features

Screen Capture: Captures the desktop, excluding the menu bar and dock on macOS.
Webcam Access: Captures webcam images with adjustable brightness and exposure.
System Information: Retrieves details like OS, CPU, and username.
File Management: Navigate directories, list files, upload files, and encrypt/decrypt files.
Remote Shell: Execute shell commands remotely.
WiFi Password Retrieval: Extract saved WiFi passwords (macOS and Windows).
Clipboard Access: Read clipboard contents.
System Control: Lock the screen (macOS and Windows).
Text-to-Speech: Convert text to speech (macOS and Windows).

Prerequisites

Python 3.12 or higher.
Telegram Bot: A Telegram bot token obtained from BotFather.
Operating System: Tested on macOS and Windows.
Dependencies:pip install mss opencv-python numpy pyttsx3 telebot pyAesCrypt secure_delete pyperclip Pillow



Installation

Clone the Repository:
git clone https://github.com/yourusername/PythonRAT.git
cd PythonRAT


Install Dependencies:Create a requirements.txt file or install dependencies manually:
pip install -r requirements.txt

Or:
pip install mss opencv-python numpy pyttsx3 telebot pyAesCrypt secure_delete pyperclip Pillow


Configure the Telegram Bot:

Create a Telegram bot via BotFather to obtain a token.
Edit PythonRAT.py and replace 'YOUR_BOT_TOKEN_HERE' with your token:TOKEN = 'your_bot_token_here'





Running the Script

Run Directly with Python:
python PythonRAT.py

This starts the bot, which listens for Telegram commands. Ensure your Python environment has all dependencies installed.

Interact via Telegram:Send commands to your Telegram bot (e.g., /start, /screen, /webcam). See the Usage section for a full list of commands.


Creating a Standalone Executable
To create a standalone executable that runs without requiring Python or dependencies, use PyInstaller.

Install PyInstaller:
pip install pyinstaller


Build the Executable:Run the following command in the project directory:
python -m PyInstaller --onefile \
--add-data "PythonRAT.py:." \
--add-data "$(python -c 'import numpy; print(numpy.__path__[0])'):numpy" \
--add-data "$(python -c 'import cv2; print(cv2.__path__[0])'):cv2" \
--hidden-import=mss \
--hidden-import=cv2 \
--hidden-import=numpy \
--hidden-import=numpy._core \
--hidden-import=numpy._core._exceptions \
--hidden-import=pyttsx3 \
--hidden-import=telebot \
--hidden-import=pyAesCrypt \
--hidden-import=secure_delete \
--hidden-import=pyperclip \
--hidden-import=xml.etree.ElementTree \
--hidden-import=PIL \
--name PythonRAT PythonRAT.py


Note: On macOS, replace the $(python -c ...) paths with your Python installation’s site-packages (e.g., /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/numpy:numpy).
On Windows, use semicolons (;) instead of colons (:) for --add-data paths (e.g., path\to\numpy;numpy).


Locate the Executable:The executable will be in the dist directory:
ls dist/PythonRAT


Run the Executable:

macOS:chmod +x dist/PythonRAT
./dist/PythonRAT


Windows:dist\PythonRAT.exe





Usage

Start the bot by running PythonRAT.py or the PythonRAT executable.

Send commands via Telegram to your bot:

/start: Initialize the bot.
/help: List available commands.
/screen: Capture a desktop screenshot (excludes menu bar and dock on macOS).
/webcam: Capture a webcam image.
/sys: Get system information.
/ip: Get public IP address.
/cd [folder]: Change directory.
/ls: List directory contents.
/upload [path]: Upload a file.
/crypt [path]: Encrypt files in a folder.
/decrypt [path]: Decrypt files in a folder.
/lock: Lock the screen.
/clipboard: Read clipboard contents.
/shell: Enter remote shell mode (type exit to leave).
/wifi: Retrieve WiFi passwords.
/speech [text]: Convert text to speech.


Check logs for debugging (if configured):
cat ~/Library/Logs/PythonRAT.log  # macOS
type %USERPROFILE%\PythonRAT.log  # Windows



Notes

Cross-Platform:
The script is optimized for macOS (e.g., screen capture excludes menu bar/dock, webcam brightness adjusted) but works on Windows with minor differences.
The /shutdown command is disabled on macOS to avoid sudo requirements.


File Storage: Temporary files (screenshots, webcam images) are stored in /tmp (macOS) or the current directory (Windows) and deleted after use.
Permissions: On macOS, ensure permissions for screen recording and camera are granted in System Settings > Privacy & Security. Windows may require similar permissions for webcam access.
Executable Size: The standalone executable may be large (100MB+) due to dependencies like numpy and opencv-python.

Troubleshooting

ModuleNotFoundError: Ensure all dependencies are installed in your Python environment. For the executable, verify --hidden-import flags include all required modules.
Permission Issues: On macOS, grant screen recording and camera permissions. Reset permissions if needed:sudo tccutil reset ScreenCapture
sudo tccutil reset Camera


Dark Webcam Image: Adjust CAP_PROP_BRIGHTNESS, CAP_PROP_EXPOSURE, or CAP_PROP_GAIN in the capture_webcam_image function in PythonRAT.py.
Screen Capture Issues: Modify the region in the send_screen function to adjust the captured area.
Logs: Configure logging in PythonRAT.py to debug issues (e.g., add logging.basicConfig(level=logging.DEBUG)).

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Disclaimer
This tool is provided "as is" for educational purposes. The author is not responsible for any misuse, damage, or legal consequences resulting from its use. Always obtain explicit permission before running this tool on any system.
