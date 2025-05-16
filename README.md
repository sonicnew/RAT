# RAT
Python-based Telegram-controlled RAT for Windows, with variants for persistence, screenshot, webcam, and remote shell. For educational use only.

---

## ⚙️ Requirements

- Python 3 (Windows only)
- Telegram Bot Token
- Telegram Chat ID
- `PyInstaller` (for building `.exe` files)
- Windows OS

---

## 🛠️ Setup

1. **Create a Telegram Bot** via [@BotFather](https://t.me/BotFather) and copy the `TOKEN`.
2. Get your **Chat ID** using [this tool](https://api.telegram.org/bot<YourBotToken>/getUpdates) .
3. Open the Python file and update:
   ```python
   TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
   ```

4. Optional: Compile the script into an executable for Windows:
   ```bash
   pyinstaller --noconsole --onefile your_script.py
   ```

---

## 📁 Folder Structure

- **Folder 1 - Full Version with Persistence:**
  - Adds persistence (starts with Windows).
  - Works even after system restart .

- **Folder 2 - No Persistence, Extended Features:**
  - Lighter version without auto-start.
  - Commands:
    - `/cmd`
    - `/screenshot`
    - `/webcam`
    - `/shutdown`
  - Smaller codes with selected features.  
    You can download and explore it to see the available functionalities.


- **Folder 3 - Minimal Version (CMD only):**
  - Very lightweight version.
  - Only supports:
    - `/cmd`
  - Ideal for testing or quick shell access scenarios.

---

## 🧪 Usage

> **Note:** This RAT works only on **Windows** and should be used in lab or test environments.

1. Modify the Python code with your Telegram credentials.
2. Run the script or build it into an EXE.
3. Control it via Telegram using commands like `/cmd`, `/screenshot`, etc.

## ⚠️ Disclaimer

This project is created **for educational and ethical research purposes only.**  
It is meant to demonstrate how attackers may implement Telegram-based RATs, and help defenders recognize and understand such behaviors.

**The author is not responsible for any misuse of this code.**  
Do **not** use this on systems you do not own or have permission to test.

Using this software for malicious purposes is illegal and unethical.
