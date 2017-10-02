from __future__ import absolute_import, unicode_literals

from clients.instagram import build_instagram_client_using_env_variables
from clients.open_weather import build_open_weather_client_using_env_variables
from clients.sky_scanner import build_sky_scanner_client_from_env_vars
from clients.uber import build_uber_client_using_env_variables
from commons.conversion import parse_date
from commons.logs import get_logger
from commons.model import Location, City
from .celery import app

logger = get_logger()


@app.task
def retrieve_weather(location_dict):
    """
    :type location_dict: dict
    :rtype: list[dict]
    """
    location = Location.from_serializable(location_dict)
    client = build_open_weather_client_using_env_variables()
    forecasts = client.get_5_days_forecast(location)
    return [f.to_serializable() for f in forecasts]


@app.task
def retrieve_instagram_media(city_dict):
    """
    :type city_dict: dict
    :rtype: list[dict]
    """
    city = City.from_serializable(city_dict)
    client = build_instagram_client_using_env_variables()
    instagram_media_list = client.recent_photos_from(city=city)
    return [m.to_serializable() for m in instagram_media_list]


@app.task
def retrieve_sky_scanner_flights(city_a_dict, city_b_dict, outbound_date_iso):
    """
    :type city_a_dict: dict
    :type city_b_dict: dict
    :type outbound_date_iso: str
    :rtype: list[dict]
    """
    client = build_sky_scanner_client_from_env_vars()
    city_a = City.from_serializable(city_a_dict)
    city_b = City.from_serializable(city_b_dict)
    outbound_date = parse_date(outbound_date_iso)
    sky_scanner_flights = client.find_flights_for_month(city_a.city_code, city_b.city_code, outbound_date.date())
    return [f.to_serializable() for f in sky_scanner_flights]


@app.task
def retrieve_uber_3km_pricing(location_dict):
    """
    :type location_dict: dict
    :rtype: list[dict]
    """
    location = Location.from_serializable(location_dict)
    uber_client = build_uber_client_using_env_variables()
    uber_pricing_list = uber_client.estimate_3km_price(location)
    return [p.to_serializable() for p in uber_pricing_list]
