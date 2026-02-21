locations = ['India', 'England', 'Russia', 'Spain', 'Italy']

# Original order
print(locations)

# Alphabetical order (without modifying original list)
print(sorted(locations))

# Still original order
print(locations)

# Reverse alphabetical (without modifying original list)
print(sorted(locations, reverse=True))

# Still original order
print(locations)

# Reverse the list (modify original)
locations.reverse()
print(locations)

# Reverse again (back to original)
locations.reverse()
print(locations)

# Sort alphabetically (modify original)
locations.sort()
print(locations)

# Sort reverse alphabetically (modify original)
locations.sort(reverse=True)
print(locations)