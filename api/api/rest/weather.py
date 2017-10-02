from commons.api_abstraction import RestApi
from commons.model import City


class WeatherApi(RestApi):
    def __init__(self, service, places_list, logger=None):
        """
        :type service: api.celery_service.CeleryService
        :type places_list: list[commons.model.City]
        :type logger: logging.Logger
        """
        super(WeatherApi, self).__init__(logger)
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
        city = City.from_serializable(request_payload)
        self.logger.info("API: getting weather for: {}...".format(city))
        return self.service.get_weather_forecast(city.location)
