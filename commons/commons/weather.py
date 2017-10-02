from commons.conversion import utc_timestamp_to_datetime
from commons.model import Model


def build_weather_5_day_forecast_object(weather_dict):
    """
    :type weather_dict:
    :rtype: commons.weather.Weather5DayForecast
    """
    forecast_timestamp = int(weather_dict.get("dt"))
    temperature = float(weather_dict.get("main").get("temp"))
    pressure = float(weather_dict.get("main").get("pressure"))
    humidity = int(weather_dict.get("main").get("humidity"))
    weather_conditions = weather_dict.get("weather")
    weather_name = weather_conditions[0].get("main") if weather_conditions else ""
    weather_desc = weather_conditions[0].get("description") if weather_conditions else ""
    wind_speed = float(weather_dict.get("wind").get("speed"))
    cloudiness = int(weather_dict.get("clouds").get("all"))
    return Weather5DayForecast(timestamp=forecast_timestamp, temperature=temperature, humidity=humidity,
                               pressure=pressure, wind_speed=wind_speed, cloudiness=cloudiness,
                               weather_name=weather_name, weather_desc=weather_desc)


class Weather5DayForecast(Model):
    def __init__(self, timestamp, temperature, humidity, pressure, wind_speed, cloudiness, weather_name, weather_desc):
        """
        :type timestamp: int
        :type temperature: float
        :type humidity: int
        :type pressure: float
        :type wind_speed: float
        :type cloudiness: int
        :type weather_name: str
        :type weather_desc: str
        """
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.cloudiness = cloudiness
        self.weather_name = weather_name
        self.weather_desc = weather_desc

    @property
    def weather_description(self):
        """
        :rtype: str
        """
        return "{} ({})'".format(self.weather_name, self.weather_desc)

    @property
    def forecast_utc_time(self):
        """
        :rtype: datetime.datetime
        """
        return utc_timestamp_to_datetime(self.timestamp)
