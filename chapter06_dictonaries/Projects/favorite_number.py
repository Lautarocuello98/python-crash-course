favorite_numbers = {
    "Lautaro": [7, 10, 21],
    "Maria": [3, 9],
    "John": [5]
}

for name, numbers in favorite_numbers.items():
    if len(numbers) == 1:
        print(f"\n{name}'s favorite number is:")
        for number in numbers:
            print(number)
    else:
        print(f"\n{name}'s favorite numbers are:")
        for i, number in enumerate(numbers):
            if i < len(numbers) - 1:
                print(number, end=', ')
            else:
                print(number)