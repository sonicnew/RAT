````
# Remote telegram control 

This is an **educational Python-based tool** that demonstrates how to send remote automation commands to a Windows system using Telegram.

> ❗ This project is intended solely for cybersecurity education, blue team training, and controlled lab simulations.

---

## 🔧 Requirements

- Python 3 (Windows)
- Telegram Bot Token (from @BotFather)
- Telegram Chat ID
- PyInstaller (optional, for .exe build)
- Windows OS

---

## 🛠️ Setup Instructions

1. Create a Telegram Bot using [@BotFather](https://t.me/BotFather).
2. Get your Telegram Chat ID (you can use tools like `userinfobot`).
3. Open any version of `automation.py` and update the following lines:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
````

4. (Optional) Compile the script to `.exe` using:

```bash
pyinstaller --noconsole --onefile automation.py
```

---

## 📁 Versions Explained

### 🔹 Version\_AutoStart

* Runs automatically .
* Useful for persistence analysis in lab setups.

### 🔹 Version\_ManualRun

* Standard execution via terminal.
* Supports screenshot and webcam snapshot.

### 🔹 Version\_CLIOnly

* Lightweight version for command-line only tasks.

---

## ✅ Supported Commands

These can be sent to the bot via Telegram:

* `/cmd` – Run a system command
* `/screenshot` – Take a screenshot
* `/webcam` – Capture a webcam image
* `/shutdown` – Log off or shut down the system

> All code is written for testing and training within isolated environments.

---

## ⚠️ Disclaimer

This software is created strictly for:

* Blue team awareness and defensive testing
* Cybersecurity educational purposes
* Malware analysis and behavioral research

**Do not use on real systems or without permission.**

The author does **not support or condone** misuse of this tool in any form.

Using this project for malicious purposes is illegal and violates GitHub's Acceptable Use Policy.

```

---
