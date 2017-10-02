from commons.model import City, Location

DEFAULT_CITIES = [
    City(city_name="Berlin",
         population=3671000,
         location=Location(52.52000659999999, 13.404953999999975),
         country="Germany",
         city_code="BERL-sky"),
    City(city_name="London",
         population=8673713,
         location=Location(51.5073509, -0.12775829999998223),
         country="United Kingdom",
         city_code="LOND-sky"),
    City(city_name="Paris",
         population=2244000,
         location=Location(48.85661400000001, 2.3522219000000177),
         country="France",
         city_code="PARI-sky")
]
