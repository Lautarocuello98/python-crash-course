responses = {}

polling_active = True

while polling_active:
    name = input("What is your name? ")
    vacation = input("If you could visit one place in the world, where would you go? ")

    responses[name] = vacation

    repeat = input("Would you like to let another person respond? (yes/no) ")
    if repeat.lower() == "no":
        polling_active = False

print("\n--- Poll Results ---")
for name, vacation in responses.items():
    print(f"{name} would like to visit {vacation}.")