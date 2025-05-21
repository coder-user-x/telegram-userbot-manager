import asyncio
import json
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

USERS_FILE = "bot/users.json"

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

async def start_userbot(user):
    session = user["session"]
    api_id = int(user["api_id"])
    api_hash = user["api_hash"]
    owner_id = int(user["owner_id"])
    offline = user.get("offline", False)
    offline_msg = user.get("offline_msg", "I'm currently offline.")
    specific_offline = user.get("specific_offline", {})

    client = TelegramClient(StringSession(session), api_id, api_hash)

    @client.on(events.NewMessage)
    async def handler(event):
        sender = await event.get_sender()
        sender_id = sender.id

        if sender_id == owner_id:
            return  # ignore owner's own messages

        # DMs
        is_dm = event.is_private

        # Mentions or Replies
        is_mention_or_reply = (
            event.is_group or event.is_channel
        ) and (
            event.message.mentioned or
            (event.reply_to_msg_id and (await event.get_reply_message()).sender_id == (await client.get_me()).id)
        )

        if offline:
            if str(sender_id) in specific_offline:
                await event.reply(specific_offline[str(sender_id)])
            elif is_dm or is_mention_or_reply:
                try:
                    await client.send_message("me", f"Offline message from {sender_id}:\n\n{event.text}")
                    await event.reply(offline_msg)
                except Exception as e:
                    print(f"Error sending to saved messages: {e}")

        # If user replies "/online" to a message, remove specific offline
        if event.is_reply and "/online" in event.raw_text.lower():
            reply_msg = await event.get_reply_message()
            target_id = str(reply_msg.sender_id)
            if target_id in specific_offline:
                specific_offline.pop(target_id)
                user["specific_offline"] = specific_offline
                with open(USERS_FILE, "w") as f:
                    json.dump(users, f, indent=4)
                await event.reply("That user is now marked as online.")

    await client.start()
    print(f"[+] {owner_id} userbot running")
    await client.run_until_disconnected()

async def main():
    global users
    users = load_users()
    tasks = []

    for user in users:
        try:
            tasks.append(start_userbot(user))
        except Exception as e:
            print(f"Failed to start userbot for {user.get('owner_id')}: {e}")

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
