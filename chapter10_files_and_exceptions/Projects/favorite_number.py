from pathlib import Path
import json

def get_stored_number(path):
    if path.exists():
        contents = path.read_text()
        number = json.loads(contents)
        return number
    else:
        return None
    
def get_new_number(path):
    number = int(input('What is the number? '))
    contents = json.dumps(number)
    path.write_text(contents)
    return number
    

    
def greet_user():
    path = Path('number.json')
    number = get_stored_number(path)
    if number:
        print(f"Welcome back, your number is {number}!")
    else:
        number = get_new_number(path)
        print(f"We'll remember the number {number}!")

greet_user()