import json
import os

DB_FILE = "database.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    data = load_data()
    str_id = str(user_id)
    
    if str_id not in data:
        data[str_id] = {
            "wallet": 500,
            "bank": 0,
            "work_cooldown": 0
        }
        save_data(data)
    
    return data[str_id]

def update_user(user_id, key, amount):
    data = load_data()
    str_id = str(user_id)
    
    if str_id not in data:
        get_user(user_id)
        data = load_data()
        
    data[str_id][key] += amount
    save_data(data)

def set_user_money(user_id, key, amount):
    data = load_data()
    str_id = str(user_id)
    
    if str_id not in data:
        get_user(user_id)
        data = load_data()
        
    data[str_id][key] = amount
    save_data(data)
