available_toppings = ['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese']

requested_toppings = ['mushrooms', 'french fries', 'extra cheese', 'pepperoni']

for toping in requested_toppings:
    if toping in available_toppings:
        print(f"Adding {toping}..")
    else:
        print(f"Sorry, we are out of {toping} right now")

print("\nFinished making your pizza!")

 