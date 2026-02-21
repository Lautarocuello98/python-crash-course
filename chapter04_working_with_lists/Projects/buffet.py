
# Original menu (tuple)
menu = ('pizza', 'pasta', 'salad', 'rice', 'soup')

print("Original menu:")
for food in menu:
    print(food)

# Try to modify one item (this will cause an error)

# The restaurant changes two items
menu = ('pizza', 'pasta', 'burger', 'rice', 'ice cream')

print("\nRevised menu:")
for food in menu:
    print(food)