from pathlib import Path
import json

def get_stored_user_data(path):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return None
    return None
    
def get_new_user_data(path):
    username = input('What is your name? ').strip().title()
    city = input("What is your city? ").strip().title()
    job = input("What is your job? ").strip().title()

    data = {
        "username": username,
        "city": city,
        "job": job
    }
    
    path.write_text(json.dumps(data))
    return data

    
def greet_user_data():
    path = Path('data.json')
    user_data = get_stored_user_data(path)

    if user_data:
        print(f"I found this user: {user_data['username']}.")

        confirm = input("Is this you? (yes/no) ").strip().lower()
        if confirm in ("yes", "y", "si", "sí"):
            print(f"Welcome back, {user_data['username']} from {user_data['city']}!")
            print(f"Still working as a {user_data['job']}?")

        else:
            user_data = get_new_user_data(path)
            print(f"We'll remember you when you come back, {user_data['username']}!")    

    else:
        user_data = get_new_user_data(path)
        print(f"We'll remember you when you come back, {user_data['username']}!")

greet_user_data()