import json
import os
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import MessageNotModifiedError

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))       # Admin user ID to allow /user_info
BOT_PASSWORD = os.getenv("BOT_PASSWORD")   # Password for registration

USERS_FILE = "users.json"

# Load users data from JSON file or initialize empty dict
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Users data structure:
# {
#   "<user_id>": {
#       "api_id": int,
#       "api_hash": str,
#       "session": str,
#       "owner_id": int,
#       "offline": false,
#       "offline_message": "I'm offline",
#       "specific_offline": {
#           "<user_id>": "custom message"
#       },
#       "online_offline_count": {"online": 0, "offline": 0}
#   }
# }

users = load_users()

client = TelegramClient('bot_session', api_id=0, api_hash='')  # no need api_id/hash for bot, so dummy

# We'll keep track of registration states here (in-memory)
# Format: {user_id: {"step": str, "data": dict}}
registrations = {}

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Welcome! Use /help to see commands.")

@client.on(events.NewMessage(pattern="/help"))
async def help_handler(event):
    text = (
        "Commands:\n"
        "/create_account - Register your userbot account (password protected)\n"
        "/offline - Set your userbot offline\n"
        "/online - Set your userbot online\n"
        "/set_specific_offline <user_id> <message> - Set offline message for specific user\n"
        "/remove_specific_offline <user_id> - Remove specific offline message for a user\n"
        "/user_info - (Admin only) Show all registered users info\n"
        "/help - Show this help message"
    )
    await event.reply(text)

@client.on(events.NewMessage(pattern="/create_account"))
async def create_account(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id in registrations:
        await event.reply("You are already in registration process. Please complete it or cancel.")
        return
    await event.reply("Please enter the bot password to proceed:")
    registrations[user_id] = {"step": "password", "data": {}}

@client.on(events.NewMessage)
async def registration_handler(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id not in registrations:
        return  # Not in registration mode

    state = registrations[user_id]
    step = state["step"]
    text = event.text.strip()

    if step == "password":
        if text != BOT_PASSWORD:
            await event.reply("Incorrect password. Registration canceled.")
            registrations.pop(user_id)
            return
        await event.reply("Password accepted.\nPlease enter your API ID (a number):")
        state["step"] = "api_id"

    elif step == "api_id":
        if not text.isdigit():
            await event.reply("API ID must be a number. Please enter your API ID:")
            return
        state["data"]["api_id"] = int(text)
        await event.reply("Got it. Now enter your API HASH:")
        state["step"] = "api_hash"

    elif step == "api_hash":
        if len(text) < 10:
            await event.reply("API HASH seems too short. Please enter your API HASH:")
            return
        state["data"]["api_hash"] = text
        await event.reply("Now enter your STRING SESSION:")
        state["step"] = "session"

    elif step == "session":
        if len(text) < 10:
            await event.reply("String Session seems too short. Please enter a valid session string:")
            return
        state["data"]["session"] = text
        await event.reply("Finally, enter your OWNER ID (your Telegram user ID):")
        state["step"] = "owner_id"

    elif step == "owner_id":
        if not text.isdigit():
            await event.reply("Owner ID must be a number. Please enter your OWNER ID:")
            return
        state["data"]["owner_id"] = int(text)

        # Save user data
        users[user_id] = {
            "api_id": state["data"]["api_id"],
            "api_hash": state["data"]["api_hash"],
            "session": state["data"]["session"],
            "owner_id": state["data"]["owner_id"],
            "offline": False,
            "offline_message": "I'm currently offline. Will reply later.",
            "specific_offline": {},
            "online_offline_count": {"online": 0, "offline": 0}
        }
        save_users(users)
        registrations.pop(user_id)
        await event.reply("Account registered successfully! Use /offline and /online to toggle status.")

@client.on(events.NewMessage(pattern="/offline"))
async def go_offline(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id not in users:
        await event.reply("You have no registered account. Use /create_account first.")
        return
    if users[user_id]["offline"]:
        await event.reply("You are already offline.")
        return
    users[user_id]["offline"] = True
    users[user_id]["online_offline_count"]["offline"] += 1
    save_users(users)
    await event.reply("Your userbot is now set to OFFLINE.")

@client.on(events.NewMessage(pattern="/online"))
async def go_online(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id not in users:
        await event.reply("You have no registered account. Use /create_account first.")
        return
    if not users[user_id]["offline"]:
        await event.reply("You are already online.")
        return
    users[user_id]["offline"] = False
    users[user_id]["online_offline_count"]["online"] += 1
    save_users(users)
    await event.reply("Your userbot is now set to ONLINE.")

@client.on(events.NewMessage(pattern=r"/set_specific_offline (\d+) (.+)"))
async def set_specific_offline(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id not in users:
        await event.reply("You have no registered account. Use /create_account first.")
        return
    match = event.pattern_match
    target_user = match.group(1)
    message = match.group(2).strip()
    if not message:
        await event.reply("Please provide a message after the user_id.")
        return
    users[user_id]["specific_offline"][target_user] = message
    save_users(users)
    await event.reply(f"Set specific offline message for user {target_user}.")

@client.on(events.NewMessage(pattern=r"/remove_specific_offline (\d+)"))
async def remove_specific_offline(event):
    sender = await event.get_sender()
    user_id = str(sender.id)
    if user_id not in users:
        await event.reply("You have no registered account. Use /create_account first.")
        return
    match = event.pattern_match
    target_user = match.group(1)
    if target_user in users[user_id]["specific_offline"]:
        users[user_id]["specific_offline"].pop(target_user)
        save_users(users)
        await event.reply(f"Removed specific offline message for user {target_user}.")
    else:
        await event.reply(f"No specific offline message found for user {target_user}.")

@client.on(events.NewMessage(pattern="/user_info"))
async def user_info(event):
    sender = await event.get_sender()
    if sender.id != ADMIN_ID:
        await event.reply("You are not authorized to use this command.")
        return

    if not users:
        await event.reply("No registered users found.")
        return

    info_lines = []
    for uid, data in users.items():
        info_lines.append(
            f"User ID: {uid}\n"
            f"Owner ID: {data['owner_id']}\n"
            f"Offline: {data['offline']}\n"
            f"Offline Msg: {data['offline_message']}\n"
            f"Specific Offline Msgs: {len(data['specific_offline'])}\n"
            f"Online count: {data['online_offline_count']['online']}, Offline count: {data['online_offline_count']['offline']}\n"
            "-----"
        )
    await event.reply("\n".join(info_lines))

client.start(bot_token=BOT_TOKEN)
print("Bot is running...")
client.run_until_disconnected()
