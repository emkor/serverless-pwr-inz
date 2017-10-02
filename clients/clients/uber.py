from uber_rides.session import Session
from uber_rides.client import UberRidesClient

from commons.conversion import distance
from commons.model import Location
from commons.os_utils import get_env_variable
from commons.uber import build_uber_product_object, build_uber_pricing_object

UBER_SERVER_TOKEN_ENV_NAME = "UBER_SERVER_TOKEN"
DELTA_COORDINATES_FOR_3_KM = .0191


def build_uber_client_using_env_variables():
    """
    :rtype: clients.uber.UberClient
    """
    server_token = get_env_variable(UBER_SERVER_TOKEN_ENV_NAME)
    return UberClient(server_token)


class UberClient(object):
    def __init__(self, server_token):
        """
        :type server_token: str
        """
        self.client = UberRidesClient(Session(server_token=server_token), sandbox_mode=True)

    def get_available_products(self, location):
        """
        :type location: commons.model.Location
        :rtype: list[commons.uber.UberProduct]
        """
        response = self.client.get_products(location.latitude, location.longitude)
        if response.status_code == 200:
            return map(lambda product: build_uber_product_object(product), response.json.get('products'))
        else:
            raise self._build_error_from_response(response)

    def estimate_price(self, location_a, location_b):
        """
        :type location_a: commons.model.Location
        :type location_b: commons.model.Location
        :rtype: list[commons.uber.UberPricing]
        """
        response = self.client.get_price_estimates(location_a.latitude, location_a.longitude,
                                                   location_b.latitude, location_b.longitude)
        if response.status_code == 200:
            return map(lambda pricing: build_uber_pricing_object(pricing), response.json.get("prices"))
        else:
            raise self._build_error_from_response(response)

    def estimate_3km_price(self, location_a):
        """
        :type location_a: commons.model.Location
        :rtype: list[commons.uber.UberPricing]
        """
        location_b = Location(latitude=location_a.latitude + DELTA_COORDINATES_FOR_3_KM,
                              longitude=location_a.longitude + DELTA_COORDINATES_FOR_3_KM)
        response = self.client.get_price_estimates(location_a.latitude, location_a.longitude,
                                                   location_b.latitude, location_b.longitude)
        if response.status_code == 200:
            return map(lambda pricing: build_uber_pricing_object(pricing), response.json.get("prices"))
        else:
            raise self._build_error_from_response(response)

    @staticmethod
    def _build_error_from_response(response):
        return IOError("Could not retrieve information from Uber. Code: {} error: {}".format(response.status_code,
                                                                                             response.json))


print(distance(Location(1.0, 1.0), Location(1.0 + DELTA_COORDINATES_FOR_3_KM, 1.0 + DELTA_COORDINATES_FOR_3_KM)))
