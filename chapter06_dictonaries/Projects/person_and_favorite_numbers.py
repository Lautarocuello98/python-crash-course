person = {'first_name': 'lautaro', 'last_name': 'cuello', 'age': 28, 'city': 'Buenos Aires'}

for key, value in person.items():
    print(f"{key}: {value}")

favorite_numbers = {
    'lili': 7,
    'yaz': 13,
    'dani': 21,
    'lau': 23,
    'marce': 5,
    }

print('\nFavorite numbers:')
for key, value in favorite_numbers.items():
    print(f'{key}: {value}')