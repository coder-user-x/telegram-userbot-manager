# Telegram Multi-Account Offline/Online Userbot System

This project provides a **Telegram management bot** to register multiple user accounts and a **userbot runner** that manages these accounts' online/offline status with customizable offline messages.

---

## Features

### Management Bot (`bot/bot.py`)
- Register user accounts by providing API ID, API Hash, String Session, and Owner ID.
- Password-protected registration (set via environment variable).
- Toggle userbot status with `/online` and `/offline` commands.
- Set global offline message and specific offline messages for individual users.
- Admin-only `/userinfo` command to view all registered users and their status.
- Stores all user data securely in `bot/users.json`.

### Userbot Runner (`userbot_runner/main.py`)
- Loads all registered users and runs a Telethon session for each.
- Automatically replies with offline messages when offline.
- Saves messages from users who contact while offline into "Saved Messages".
- Supports toggling individual userbots online/offline.
- Supports specific offline messages per contact.

---

## Project Structure

/your-project-root │ ├── bot/ │   ├── bot.py             # Telegram bot for managing user accounts │   ├── users.json         # JSON file storing user data and status │   └── utils.py           # Helper functions for JSON file operations │ ├── userbot_runner/ │   └── main.py            # Runs userbots for all registered accounts │ ├── .env                   # Environment variables for bot configuration ├── requirements.txt       # Python dependencies └── README.md              # Project overview and instructions

---

## Setup Instructions

### 1. Create `.env` file with the following variables:

BOT_TOKEN=your_telegram_bot_token BOT_PASSWORD=your_secure_password ADMIN_ID=your_telegram_user_id

- `BOT_TOKEN`: The token of your Telegram bot used for account management.
- `BOT_PASSWORD`: Password users must provide to register accounts.
- `ADMIN_ID`: Telegram user ID that can run admin commands like `/userinfo`.

---

### 2. Install dependencies:

```bash
pip install -r requirements.txt


---

3. Run the management bot:

python bot/bot.py


---

4. Run the userbot runner:

python userbot_runner/main.py


---

Important Notes

String Session: This is required to log into user accounts without re-authentication. It can be generated via Telethon or external tools. Sessions do not expire unless revoked or logged out.

Data Persistence: All user data is saved in bot/users.json.

Telegram Rules: Automated replies and userbots should follow Telegram’s Terms of Service. Abuse may lead to account restrictions or bans.

Security: Protect your .env file and users.json as they contain sensitive information.



---

License

MIT License

If you want me to generate the file content as an actual `.md` file you can save, just let me know!

