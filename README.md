# Decima

Telegram bot powered by GeoNames API.

## Setup

### 1. Create a Telegram Bot

Open Telegram and message **@BotFather**.

Create a new bot using:

```text
/newbot
```

BotFather will send you a token. Save it.

---

### 2. Create a GeoNames Account

Register a free account:

https://www.geonames.org/

Save your GeoNames username.

---

### 3. Clone the Repository

```bash
git clone https://github.com/paulruru/Decima.git
cd Decima
```

---

### 4. Create and Activate a Virtual Environment

**Windows (Git Bash)**

```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Create a `.env` File

Create a file named `.env` in the project root (next to `main.py`).

```env
BOT_TOKEN=your_bot_token
GEO_NAME=your_geonames_username
```

Example:

```env
BOT_TOKEN=123456789:ABCDEF...
GEO_NAME=johndoe
```

---

### 7. Run the Bot

```bash
python main.py
```

If everything is configured correctly, the bot will start and be ready to receive messages.

## Requirements

* Python 3.10+
* Telegram Bot Token
* GeoNames Account
