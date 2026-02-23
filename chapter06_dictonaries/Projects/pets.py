pet1 = {"animal": "dog", "owner": "Lautaro"}
pet2 = {"animal": "cat", "owner": "Maria"}
pet3 = {"animal": "parrot", "owner": "John"}

pets = [pet1, pet2, pet3]

for pet in pets:
    print("\nPet info:")
    for key, value in pet.items():
        print(f"{key}: {value}")