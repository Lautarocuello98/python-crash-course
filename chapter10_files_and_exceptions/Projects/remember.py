# Lautarocuello98

from pathlib import Path
from datetime import datetime
import json

DATA_PATH = Path("user") / "data.json"

def load_user(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

def save_user(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def prompt_user():
    return {
        "username": input("Name: ").strip().title(),
        "city": input("City: ").strip().title(),
        "job": input("Job: ").strip().title(),
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

def main():
    user = load_user(DATA_PATH)

    if user:
        print(f"Found user: {user.get('username','Unknown')} "
              f"({user.get('city','Unknown')}, {user.get('job','Unknown')}) - "
              f"Last seen: {user.get('last_seen','N/A')}")
        if input("Is this you? (y/n) ").strip().lower() in ("y","yes","si","sí"):
            user["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_user(DATA_PATH, user)
            print(f"Welcome back, {user.get('username','there')} 👋")
            return

    user = prompt_user()
    save_user(DATA_PATH, user)
    print(f"Saved in {DATA_PATH}. See you next time, {user['username']}!")

if __name__ == "__main__":
    main()