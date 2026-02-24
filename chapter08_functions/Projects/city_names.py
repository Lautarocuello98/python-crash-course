def city_country(city, country):
    complete = {'city': city, 'country': country}
    return complete

record = []

while True:
    print("Tell me cities with each country: ")
    print("press q to quit")

    input_city = input("What city? ")
    if input_city == 'q':
        break

    input_country = input("What country: ")
    if input_country == 'q':
        break

    record.append(city_country(input_city.title(), input_country.title()))

for item in record:
    print(f'{item['city']}, {item['country']}')