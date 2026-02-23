favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
}
friends = ['phil', 'sarah']

for name in favorite_languages.keys():
    print(f"Hi {name.title()}")

    if name in friends:
        print(f"\t{name.title()}, I see you love {favorite_languages[name].title()}")