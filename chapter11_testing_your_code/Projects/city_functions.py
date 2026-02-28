def city_country(city, country, population=None):
    if population:
        return f"{city.title()}, {country.title()} - population {population}"
    return f"{city.title()}, {country.title()}"