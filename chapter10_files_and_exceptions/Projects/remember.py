#Lautarocuello98

from pathlib import Path
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
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def prompt_user():
    return {
        "username": input("Name: ").strip().title(),
        "city": input("City: ").strip().title(),
        "job": input("Job: ").strip().title(),
    }


def main():
    user = load_user(DATA_PATH)

    if user:
        print(f"Found user: {user['username']} ({user['city']}, {user['job']})")
        if input("Is this you? (y/n) ").strip().lower() in ("y", "yes", "si", "sí"):
            print(f"Welcome back, {user['username']} 👋")
            return

    user = prompt_user()
    save_user(DATA_PATH, user)
    print(f"Saved in {DATA_PATH}. See you next time, {user['username']}!")


if __name__ == "__main__":
    main()