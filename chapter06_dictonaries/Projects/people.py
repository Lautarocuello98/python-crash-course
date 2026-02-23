person1 = {
    "first_name": "Lautaro",
    "last_name": "Cuello",
    "age": 25,
    "city": "San Francisco"
}

person2 = {
    "first_name": "Maria",
    "last_name": "Lopez",
    "age": 30,
    "city": "Madrid"
}

person3 = {
    "first_name": "John",
    "last_name": "Smith",
    "age": 40,
    "city": "New York"
}

people = [person1, person2, person3]

for person in people:
    print("\nPerson info:")
    for key, value in person.items():
        print(f"{key}: {value}")