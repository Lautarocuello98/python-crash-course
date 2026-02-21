# Create a list from 1 to 1,000,000
numbers = list(range(1, 1_000_001))

# be sure the min and max
if min(numbers) == 1 and max(numbers) == 1000000:

    # Print each number using a for loop
    for number in numbers:
        print(number)