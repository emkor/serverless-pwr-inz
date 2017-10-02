import requests

from commons.backend_service import BackendService
from commons.instagram import InstagramMedia
from commons.sky_scanner import Flight
from commons.uber import UberPricing
from commons.weather import Weather5DayForecast


class LambdaService(BackendService):
    def __init__(self, logger, base_service_url):
        """
        :type logger: logging.Logger
        :type base_service_url: str
        """
        super(LambdaService, self).__init__()
        self.logger = logger
        self.service_url = base_service_url

    def get_weather_forecast(self, location):
        """
        :type location: commons.model.Location
        :rtype: list[commons.weather.Weather5DayForecast]
        """
        self.logger.info("Retrieving weather for: {}...".format(location))
        function_url = self._get_function_url("weather")
        response = requests.post(url=function_url, json=location.to_serializable())
        if response.ok:
            self.logger.info("Weather retrieval for {} done!".format(location))
            return [Weather5DayForecast.from_serializable(f) for f in response.json()]
        else:
            self.logger.error(
                "Could not retrieve weather forecast for: {}. Details: {} {}".format(location, response.status_code,
                                                                                     response.content))
            return []

    def retrieve_instagram_media(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.instagram.InstagramMedia]
        """
        self.logger.info("Retrieving instagram media for: {}...".format(city))
        function_url = self._get_function_url("instagram")
        response = requests.post(url=function_url, json=city.to_serializable())
        if response.ok:
            self.logger.info("Instagram media retrieval for {} done!".format(city))
            return [InstagramMedia.from_serializable(f) for f in response.json()]
        else:
            self.logger.error(
                "Could not retrieve media for: {}. Details: {} {}".format(city, response.status_code,
                                                                          response.content))
            return []

    def retrieve_sky_scanner_flights(self, city_a, city_b, outbound_date):
        """
        :type city_a: commons.model.City
        :type city_b: commons.model.City
        :type outbound_date: datetime.date
        :rtype: list[commons.sky_scanner.Flight]
        """
        self.logger.info("Retrieving SkyScanner flights for: {} -> {} on: {}...".format(city_a, city_b, outbound_date))
        function_url = self._get_function_url("skyscanner")
        request = {"city_a": city_a.to_serializable(),
                   "city_b": city_b.to_serializable(),
                   "outbound_date": outbound_date.isoformat()}
        response = requests.post(url=function_url, json=request)
        if response.ok:
            sky_scanner_flights_serialized = response.json()
            self.logger.info(
                "Retrieved SkyScanner {} flights for: {} -> {} on: {}!".format(len(sky_scanner_flights_serialized),
                                                                               city_a, city_b, outbound_date))
            return [Flight.from_serializable(f) for f in sky_scanner_flights_serialized]
        else:
            self.logger.error(
                "Could not retrieve flights. Details: {} {}".format(response.status_code, response.content))
            return []

    def retrieve_uber_3km_pricing(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.uber.UberPricing]
        """
        self.logger.info("Retrieving Uber pricing for 3km from: {}...".format(city))
        function_url = self._get_function_url("uber")
        response = requests.post(url=function_url, json=city.location.to_serializable())
        if response.ok:
            uber_pricing_serialized = response.json()
            self.logger.info(
                "Retrieved {} Uber pricing for: {}!".format(len(uber_pricing_serialized), city))
            return [UberPricing.from_serializable(f) for f in uber_pricing_serialized]
        else:
            self.logger.error(
                "Could not retrieve Uber pricing for: {}. Details: {} {}".format(city, response.status_code,
                                                                                 response.content))
            return []

    def _get_function_url(self, sub_url):
        """
        :type sub_url: str
        :rtype: str
        """
        return "{}/{}".format(self.service_url, sub_url)
