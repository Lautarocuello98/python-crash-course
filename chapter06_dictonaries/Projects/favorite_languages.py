favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
}

students = ['jen', 'lili', 'dani', 'sarah', 'edward', 'lau', 'phil']

for name in students:
    if name in favorite_languages:
        print(f"Thanks {name.title()} for taking your {favorite_languages[name].title()}'s class")
    else: 
        print(f"{name.title()} you needs take class.")