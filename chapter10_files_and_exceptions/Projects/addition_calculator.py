print("Give me two numbers, and I'll multipicate them.")
print("Enter 'q' to quit")

while True:
    first_number = input("\nFirst number: ")
    try:
        first_number = int(first_number)
    except ValueError:
        print("Must be a number")
        pass
    if first_number == 'q':
        break
    second_number = input("\nSecond number: ")
    try:
        second_number = int(second_number)
    except ValueError:
        print("Must be a number")
        pass
    if second_number == 'q':
        break

    try:
        answer = int(first_number) * int(second_number)
    except TypeError, ValueError:
        print("you must use numbers")
    else:
        print(f"\n{answer}")