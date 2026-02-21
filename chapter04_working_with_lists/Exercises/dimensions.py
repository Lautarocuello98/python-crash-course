# The tupples are inmutables, we need make a new one if we want to change

dimensions = (200, 250)
print("Original dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 100)
print("\nModified dimensions:")
for dimension in dimensions:
    print(dimension)