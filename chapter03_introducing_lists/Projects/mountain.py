mountains = ['Everest', 'K2', 'Kilimanjaro', 'Denali', 'Fuji']

# Print original list
print(mountains)

# len()
print("Number of mountains:", len(mountains))

# append()
mountains.append('Matterhorn')
print(mountains)

# insert()
mountains.insert(0, 'Aconcagua')
print(mountains)

# del
del mountains[2]
print(mountains)

# pop()
popped_mountain = mountains.pop()
print("Popped:", popped_mountain)
print(mountains)

# remove()
mountains.remove('Fuji')
print(mountains)

# sorted() (does not modify original)
print("Alphabetical:", sorted(mountains))
print("Still original:", mountains)

# reverse()
mountains.reverse()
print("Reversed:", mountains)

# sort()
mountains.sort()
print("Sorted:", mountains)

# sort(reverse=True)
mountains.sort(reverse=True)
print("Reverse sorted:", mountains)