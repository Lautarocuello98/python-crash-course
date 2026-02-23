while True:
    topping = input("Enter a pizza topping (type 'quit' to exit): ")

    if topping.lower() == "quit":
        break

    print(f"I'll add {topping} to your pizza.")