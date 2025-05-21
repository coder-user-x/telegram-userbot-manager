import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user_id, api_id, api_hash, session, owner_id):
    users = load_users()
    users[str(user_id)] = {
        "api_id": int(api_id),
        "api_hash": api_hash,
        "session": session,
        "owner_id": int(owner_id),
        "offline": False,
        "offline_message": "I'm currently offline.",
        "specific_offline": {},
        "stats": {
            "times_online": 0,
            "times_offline": 0
        }
    }
    save_users(users)

def update_user(user_id, key, value):
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)][key] = value
        save_users(users)

def get_user(user_id):
    users = load_users()
    return users.get(str(user_id), None)

def delete_user(user_id):
    users = load_users()
    if str(user_id) in users:
        del users[str(user_id)]
        save_users(users)
