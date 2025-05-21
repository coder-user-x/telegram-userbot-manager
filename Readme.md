# Multi-Account Telegram Offline/Online Userbot

This project is a dual system:
- A **Telegram bot** that lets users register their own Telegram accounts (via String Session, API ID/Hash) after passing a password.
- A **userbot runner** that keeps those accounts online, responds with offline messages, and syncs back online status when owners reply.

---

## Features

### Telegram Bot (`/bot`)
- `/start`: Begin interaction and registration
- Collects `API ID`, `API HASH`, `Session`, `Owner ID`
- Password-protected via `.env`
- Tracks:
  - Offline/Online status
  - Custom offline messages
  - Specific user offline messages
- Only the admin (set in `.env`) can run `/userinfo` to view all registered accounts.

### Userbot Runner (`/userbot_runner`)
- Loads all users from `bot/users.json`
- Starts a Telethon session per user
- Automatically replies with offline message
- Logs incoming messages to saved messages
- Users can:
  - Send `/offline` or `/online` to toggle globally
  - Set `/set_specific_offline {user_id} {message}`
  - Reply to any message with `/online` to reset specific offline

---

## Project Structure
