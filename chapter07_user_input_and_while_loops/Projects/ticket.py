while True:
    age_input = input("Enter your age (type 'quit' to exit): ")

    if age_input.lower() == "quit":
        break

    age = int(age_input)

    if age < 3:
        price = 0
    elif age <= 12:
        price = 10
    else:
        price = 15

    print(f"Your ticket costs ${price}.")