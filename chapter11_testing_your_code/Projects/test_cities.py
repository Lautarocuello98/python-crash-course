from city_functions import city_country

def test_city_country():
    results = city_country("santiago", "chile")
    assert results == "Santiago, Chile"

def test_city_country_population():
    results = city_country("santiago", "chile", 5000000)
    assert results == "Santiago, Chile - population 5000000"