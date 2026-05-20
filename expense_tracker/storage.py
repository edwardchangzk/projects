import json

users = {}


def save_users():
    try:
        with open("data/expenses.json", "w") as file:
            json.dump(users, file, indent=4)

    except OSError:
        print("Error: Could not save data.")


def load_users():
    global users

    try:
        with open("data/expenses.json", "r") as file:
            users = json.load(file)

    except FileNotFoundError:
        users = {}

    except json.JSONDecodeError:
        users = {}

    except OSError:
        users = {}
