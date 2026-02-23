car = input("What car do you want to rent? ")
print(f"Let me see if we have a {car}.")
print("...\n")

number_guests = int(input("How many people are in your dinner group? "))
if number_guests > 8:
    print("You'll have to wait for a table.")
else:
    print("Perfect, your table is ready.")
print("...\n")

number = int(input("Give me a number and I'll tell you if it is a multiple of 10 or not: "))
if number % 10 == 0:
    print(f"Yes, {number} is a multiple of 10.")
else:
    print(f"No, {number} is not a multiple of 10.")
print("...\n")