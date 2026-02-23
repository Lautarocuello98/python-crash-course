favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
}

print()

for name, language in favorite_languages.items():
    print(f"{name.title()}'s favorite language is {language.title()}")

print()

for name in favorite_languages.keys():
    print(f"{name.title()}")

print()
print("The following languages have been mentioned")
for language in set(favorite_languages.values()):
    print(f"{language.title()}")