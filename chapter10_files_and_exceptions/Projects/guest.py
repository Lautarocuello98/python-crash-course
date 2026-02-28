from pathlib import Path 

names = ''

while True:
    name = input("Give me a name? ").title()
    names += f'{name}\n'
    other = input("Do you want add another guest? ")
    if other == 'yes':
        continue
    else:
        break


path = Path('guest_book.txt')
path.write_text(names)