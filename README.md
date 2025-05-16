
# Remote Windows via Telegram

This is an **educational Python-based tool** that demonstrates how to send remote automation commands to a Windows system using Telegram.

> ❗ This project is intended solely for cybersecurity education, blue team training, and controlled lab simulations.

---

## 🔧 Requirements

- Python 3 (Windows)
- Telegram Bot Token (from @BotFather)
- Telegram Chat ID
- PyInstaller ( for .exe build)
- Windows OS

---

## 🛠️ Setup Instructions

1. Create a Telegram Bot using [@BotFather](https://t.me/BotFather).
2. Get your **Chat ID** using (https://api.telegram.org/bot<YourBotToken>/getUpdates) or a helper bot.
3. Open any version of `edu_remote.py` and update the following lines:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
```

4. Compile the script to `.exe` using:

```bash
pyinstaller --noconsole --onefile edu_remote_lab.py
```

---

## 📁 Versions Explained

### 🔹 Version_AutoStart
- Runs automatically at login.
- Useful for persistence analysis in lab setups.

### 🔹 Version_ManualRun
- Standard execution via terminal.
- Supports screenshot and webcam snapshot.

### 🔹 Version_CLIOnly
- Lightweight version for command-line only tasks.

---

## ✅ Supported Commands

These can be sent to the bot via Telegram:

- `/cmd` – Run a system command
- `/screenshot` – Take a screenshot
- `/webcam` – Capture a webcam image
- `/shutdown` – Log off or shut down the system

> All code is written for testing and training within isolated environments.

---

## ⚠️ Disclaimer

This software is created strictly for:

- Blue team awareness and defensive testing  
- Cybersecurity educational purposes  
- Malware analysis and behavioral research  

**Do not use on real systems or without permission.**

The author does **not support or condone** misuse of this tool in any form.

Using this project for malicious purposes is illegal and violates GitHub's Acceptable Use Policy.
