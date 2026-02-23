cities = {
    "Tokyo": {
        "country": "Japan",
        "population": "37 million",
        "fact": "It is the largest metropolitan area in the world."
    },
    "Paris": {
        "country": "France",
        "population": "11 million",
        "fact": "It is known as the City of Light."
    },
    "Buenos Aires": {
        "country": "Argentina",
        "population": "15 million",
        "fact": "It is famous for tango."
    }
}

for city, info in cities.items():
    print(f"\nCity: {city}")
    for key, value in info.items():
        print(f"{key}: {value}")