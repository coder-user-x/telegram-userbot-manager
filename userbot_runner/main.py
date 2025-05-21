import asyncio
import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

USERS_FILE = "users.json"
clients = {}

# Load user data
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

users = load_users()

async def setup_userbot(user_id, user_data):
    session = user_data["session"]
    api_id = user_data["api_id"]
    api_hash = user_data["api_hash"]
    owner_id = user_data["owner_id"]
    offline_status = user_data.get("offline", False)
    specific_offline = user_data.get("specific_offline", {})
    offline_message = user_data.get("offline_message", "I'm currently offline.")

    client = TelegramClient(StringSession(session), api_id, api_hash)

    @client.on(events.NewMessage)
    async def handle_message(event):
        try:
            if event.is_private and event.sender_id != owner_id:
                if users[user_id]["offline"]:
                    custom_msg = users[user_id]["specific_offline"].get(str(event.sender_id), None)
                    msg = custom_msg or users[user_id]["offline_message"]
                    await event.reply(msg)

                    # Save it to saved messages
                    try:
                        sender = await event.get_sender()
                        text = f"Message from {sender.id}:\n{event.text}"
                        await client.send_message("me", text)
                    except Exception as e:
                        print(f"Error saving message: {e}")
        except Exception as e:
            print(f"Message handling error: {e}")

    try:
        await client.start()
        print(f"Userbot for {owner_id} started.")
        clients[user_id] = client
    except Exception as e:
        print(f"Failed to start userbot for {user_id}: {e}")

async def main():
    tasks = []
    for uid, data in users.items():
        tasks.append(setup_userbot(uid, data))
    await asyncio.gather(*tasks)
    print("All userbots are active.")

    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
