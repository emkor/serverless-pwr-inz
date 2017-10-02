from datetime import datetime

from commons.api_abstraction import RestApi
from commons.model import City


class SkyScannerApi(RestApi):
    def __init__(self, service, places_list, logger=None):
        """
        :type service: api.celery_service.CeleryService
        :type places_list: list[commons.model.City]
        :type logger: logging.Logger
        """
        super(SkyScannerApi, self).__init__(logger)
        self.places_list = places_list
        self.service = service

    def get(self, request_url, query_params):
        return "ok"

    def post(self, request_url, query_params, request_payload):
        """
        :type request_url: str
        :type query_params: dict
        :type request_payload: dict
        :rtype: list
        """
        outbound_date = datetime.utcnow().date()
        city_a = City.from_serializable(request_payload.get("city_a"))
        city_b = City.from_serializable(request_payload.get("city_b"))
        self.logger.info(
            "API: getting sky scanner flights from: {} to: {} for date: {}...".format(city_a, city_b, outbound_date))
        return self.service.retrieve_sky_scanner_flights(city_a, city_b, outbound_date)
