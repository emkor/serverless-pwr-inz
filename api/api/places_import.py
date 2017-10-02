import csv

from commons.logs import get_logger
from commons.model import Location, City

CITIES_CSV = '../ServerlessPwrInz-Cities.csv'

COUNTRY_COLUMN_INDEX = 0
CITY_COLUMN_INDEX = 1
POPULATION_COLUMN_INDEX = 2
LATITUDE_COLUMN_INDEX = 3
LONGITUDE_COLUMN_INDEX = 4
SKY_SCANNER_CITY_CODE_COLUMN_INDEX = 5

logger = get_logger(calling_module="csv_improrter")


def import_from_file(csv_file_name=CITIES_CSV):
    logger.info("Opening file: {} for reading cities...".format(csv_file_name))
    cities = []
    with open(csv_file_name, 'rb') as csv_file:
        places_csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in places_csv_reader:
            if row:
                try:
                    lat = float(row[LATITUDE_COLUMN_INDEX])
                    lon = float(row[LONGITUDE_COLUMN_INDEX])
                    location = Location(latitude=lat, longitude=lon)
                    country = unicode(row[COUNTRY_COLUMN_INDEX])
                    city_name = unicode(row[CITY_COLUMN_INDEX])
                    population = int(row[POPULATION_COLUMN_INDEX])
                    city_code = str(row[SKY_SCANNER_CITY_CODE_COLUMN_INDEX])
                    city = City(city_name=city_name, population=population, location=location,
                                country=country, city_code=city_code)
                    cities.append(city)
                except Exception as e:
                    logger.warning("Could not create city from data: <{}>".format(row))
            else:
                logger.warning("Could not create city from data: {}".format(row))
    logger.info("Ended reading cities, read: {} cities.".format(len(cities)))
    return cities
