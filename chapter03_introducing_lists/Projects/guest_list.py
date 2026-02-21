guests = ['lili', 'yaz', 'dani']
for name in guests:
    print(f"This is an invitation for {name}")

print('\nA guest will not come but another will')
guests.remove('dani')
guests.append('marce')
for name in guests:
    print(f"This is an invitation for {name}")

print('\nNow we have three new guests')

guests.insert(0, 'dani')
guests.insert(3, 'lau')
guests.append('mike')

for name in guests:
    print(f"This is an invitation for {name}")

print("\nI'm sorry but only two guests can come")

guests.sort()

# quit the guest
while len(guests) > 2:
    removed = guests.pop()   # quit the last
    print(f"Sorry {removed}, you can't come.")

for name in reversed(guests):
    print(f"{name}, you're still invited!")

print(f"only {len(guests)} were invite")

