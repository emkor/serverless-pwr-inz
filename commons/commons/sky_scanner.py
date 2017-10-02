from datetime import datetime, date

from commons.conversion import parse_date
from commons.logs import get_logger
from commons.model import Model, Price

logger = get_logger()


def build_flight_query_results(api_response_dict):
    """
    :type api_response_dict: dict[str]
    :rtype: list[commons.sky_scanner.Flight]
    """
    try:
        currencies = [c.get("Code") for c in api_response_dict.get("Currencies")]
        carriers = {int(c.get("CarrierId")): c.get("Name") for c in api_response_dict.get("Carriers")}
        places = [_build_sky_scanner_place(place_dict=p) for p in api_response_dict.get("Places")]
        flights = [_build_flight(p, currency=currencies[0], places=places, carriers=carriers)
                   for p in api_response_dict.get("Quotes")]
        return flights
    except Exception as e:
        print("Error building SkyScanner API results. Details: {}. Given dict: {}".format(e, api_response_dict))
        return None


def _build_flight(flight_dict, currency, places, carriers):
    """
    :type flight_dict: dict[str]
    :type: currency: str
    :type: places: list[commons.sky_scanner.SkyScannerPlace]
    :type: carriers: dict[int, str]
    :rtype: commons.sky_scanner.Flight
    """
    try:
        origin_place_id = int(flight_dict.get("OutboundLeg").get("OriginId"))
        destination_place_id = int(flight_dict.get("OutboundLeg").get("DestinationId"))
        flight_carrier_ids = flight_dict.get("OutboundLeg").get("CarrierIds")
        carrier_name = carriers.get(int(flight_carrier_ids[0] if flight_carrier_ids else -1))
        departure_date_str = flight_dict.get("OutboundLeg").get("DepartureDate")
        departure_date_time = datetime.strptime(departure_date_str, "%Y-%m-%dT%H:%M:%S")
        return Flight(price=Price(value=flight_dict.get("MinPrice"), currency=currency),
                      origin_place=filter(lambda p: p.place_id == origin_place_id, places)[0],
                      destination_place=filter(lambda p: p.place_id == destination_place_id, places)[0],
                      departure_date=date(year=departure_date_time.year,
                                          month=departure_date_time.month,
                                          day=departure_date_time.day),
                      carrier_name=carrier_name)
    except Exception as e:
        logger.error("Could not build Flight model. Details: {} Input dict: {}".format(e, flight_dict))
        raise e


def _build_sky_scanner_place(place_dict):
    """
    :type place_dict: dict[str]
    :rtype: commons.sky_scanner.SkyScannerPlace
    """
    return SkyScannerPlace(place_id=place_dict.get("PlaceId"), name=place_dict.get("Name"),
                           city_name=place_dict.get("CityName"), city_id=place_dict.get("CityId"),
                           country_name=place_dict.get("CountryName"))


class Flight(Model):
    def __init__(self, price, origin_place, destination_place, departure_date, carrier_name):
        """
        :type price: commons.model.Price
        :type origin_place: commons.sky_scanner.SkyScannerPlace
        :type destination_place: commons.sky_scanner.SkyScannerPlace
        :type departure_date: date
        :type carrier_name: str
        """
        self.price = price
        self.origin_place = origin_place
        self.destination_place = destination_place
        self.departure_time = departure_date
        self.carrier_name = carrier_name

    @classmethod
    def from_serializable(cls, serializable):
        """
        :type serializable: dict
        :rtype: commons.sky_scanner.Flight
        """
        price = Price.from_serializable(serializable.get("price"))
        origin_place = SkyScannerPlace.from_serializable(serializable.get("origin_place"))
        destination_place = SkyScannerPlace.from_serializable(serializable.get("destination_place"))
        departure_date = parse_date(serializable.get("departure_time"))
        return Flight(price=price, origin_place=origin_place, destination_place=destination_place,
                      departure_date=departure_date, carrier_name=serializable.get("carrier_name"))

    def to_serializable(self):
        """
        :rtype: dict
        """
        output_dict = super(Flight, self).to_serializable()
        price_dict = self.price.to_serializable()
        output_dict.update({"price": price_dict})
        origin_place_dict = self.origin_place.to_serializable()
        output_dict.update({"origin_place": origin_place_dict})
        destination_place_dict = self.destination_place.to_serializable()
        output_dict.update({"destination_place": destination_place_dict})
        departure_date = self.departure_time.isoformat()
        output_dict.update({"departure_time": departure_date})
        return output_dict


class SkyScannerPlace(Model):
    def __init__(self, place_id, name, city_name, city_id, country_name):
        """
        :type place_id: int
        :type name: str
        :type city_name: str
        :type city_id: str
        :type country_name: str
        """
        self.place_id = place_id
        self.name = name
        self.city_name = city_name
        self.city_id = city_id
        self.country_name = country_name
