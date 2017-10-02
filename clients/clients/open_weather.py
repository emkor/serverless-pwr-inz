import requests

from commons.logs import get_logger
from commons.model import Location
from commons.os_utils import get_env_variable
from commons.weather import build_weather_5_day_forecast_object

OPEN_WEATHER_API_KEY_ENV_NAME = "OPEN_WEATHER_API_KEY"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/"

logger = get_logger()


def build_open_weather_client_using_env_variables():
    open_weather_api_key = get_env_variable(OPEN_WEATHER_API_KEY_ENV_NAME)
    return OpenWeatherClient(api_key=open_weather_api_key)


class OpenWeatherClient(object):
    def __init__(self, api_key, units="metric"):
        """
        :type api_key: str
        :type units: str
        """
        self.api_key = api_key
        self.units = units

    def get_5_days_forecast(self, location):
        """
        :type location: commons.model.Location
        :rtype: list[commons.weather.Weather5DayForecast]
        """
        request_sub_url = "forecast?lat={}&lon={}&units={}&appid={}".format(location.latitude, location.longitude,
                                                                            self.units, self.api_key)
        full_url = WEATHER_URL + request_sub_url
        logger.debug("Requesting weather from URL: {}...".format(full_url))
        response = requests.get(url=full_url)
        if response.ok:
            return map(lambda weather_dict: build_weather_5_day_forecast_object(weather_dict),
                       response.json().get("list"))
        else:
            raise IOError(
                "Could not retrieve information from Weather API using url: {}. Code: {} content: {}".format(full_url,
                                                                                                             response.status_code,
                                                                                                             response.content))
