from abc import abstractmethod, ABCMeta
from commons.logs import get_logger


class BackendService(object):
    __metaclass__ = ABCMeta

    def __init__(self, logger=None):
        """
        :type logger: logging.Logger
        """
        self.logger = logger or get_logger()

    @abstractmethod
    def get_weather_forecast(self, location):
        """
        :type location: commons.model.Location
        :rtype: list[commons.weather.Weather5DayForecast]
        """
        pass

    @abstractmethod
    def retrieve_instagram_media(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.instagram.InstagramMedia]
        """
        pass

    @abstractmethod
    def retrieve_sky_scanner_flights(self, city_a, city_b, outbound_date):
        """
        :type city_a: commons.model.City
        :type city_b: commons.model.City
        :type outbound_date: datetime.date
        :rtype: list[commons.sky_scanner.Flight]
        """
        pass

    @abstractmethod
    def retrieve_uber_3km_pricing(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.uber.UberPricing]
        """
        pass
