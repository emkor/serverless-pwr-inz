import json
import unittest

from commons.weather import build_weather_5_day_forecast_object, Weather5DayForecast

WEATHER_API_RESPONSE = """
{
      "dt": 1494417600,
      "main": {
        "temp": 13.56,
        "temp_min": 10.84,
        "temp_max": 13.56,
        "pressure": 1002.84,
        "sea_level": 1023.35,
        "grnd_level": 1002.84,
        "humidity": 76,
        "temp_kf": 2.72
      },
      "weather": [
        {
          "id": 803,
          "main": "Clouds",
          "description": "broken clouds",
          "icon": "04d"
        }
      ],
      "clouds": {
        "all": 80
      },
      "wind": {
        "speed": 5.11,
        "deg": 250.503
      },
      "rain": {},
      "snow": {},
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2017-05-10 12:00:00"
    }
"""


class TestWeatherObjectBuilding(unittest.TestCase):
    def setUp(self):
        self.weather_json_response = json.loads(WEATHER_API_RESPONSE)

    def test_building_weather_forecast_object(self):
        expected_object = Weather5DayForecast(timestamp=1494417600, temperature=13.56, humidity=76, pressure=1002.84,
                                              wind_speed=5.11, cloudiness=80, weather_name="Clouds",
                                              weather_desc="broken clouds")
        actual_object = build_weather_5_day_forecast_object(self.weather_json_response)
        self.assertIsNotNone(actual_object)
        self.assertEqual(expected_object, actual_object)
