import json

from clients.instagram import build_instagram_client_using_env_variables
from clients.open_weather import build_open_weather_client_using_env_variables
from clients.sky_scanner import build_sky_scanner_client_from_env_vars
from clients.uber import build_uber_client_using_env_variables
from commons.conversion import parse_date
from commons.model import Location, City
from utils import read_payload, build_response


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }


def retrieve_weather(event, context):
    """
    :type event: dict[str, str]
    :rtype: list[dict]
    """
    location = Location.from_serializable(read_payload(event))
    print("Resolving weather for: {}...".format(location))
    client = build_open_weather_client_using_env_variables()
    forecasts = client.get_5_days_forecast(location)
    print("Resolved {} forecasts for: {}!".format(len(forecasts), location))
    return build_response(payload=[f.to_serializable() for f in forecasts])


def retrieve_instagram_media(event, context):
    """
    :type event: dict[str, str]
    :rtype: list[dict]
    """
    city = City.from_serializable(read_payload(event))
    print("Resolving instagram media for: {}...".format(city))
    client = build_instagram_client_using_env_variables()
    instagram_media_list = client.recent_photos_from(city=city)
    print("Resolved {} instagram media for: {}!".format(len(instagram_media_list), city))
    return build_response([m.to_serializable() for m in instagram_media_list])


def retrieve_uber_3km_pricing(event, context):
    """
    :type event: dict
    :rtype: list[dict]
    """
    location = Location.from_serializable(read_payload(event))
    print("Resolving Uber pricing for: {}...".format(location))
    uber_client = build_uber_client_using_env_variables()
    uber_pricing_list = uber_client.estimate_3km_price(location)
    print("Resolving {} Uber pricing for: {}!".format(len(uber_pricing_list), location))
    return build_response([p.to_serializable() for p in uber_pricing_list])


def retrieve_sky_scanner_flights(event, context):
    """
    :type event: dict
    :rtype: list[dict]
    """
    request_payload = read_payload(event)
    city_a = City.from_serializable(request_payload.get("city_a"))
    city_b = City.from_serializable(request_payload.get("city_b"))
    outbound_date = parse_date(request_payload.get("outbound_date"))
    client = build_sky_scanner_client_from_env_vars()
    sky_scanner_flights = client.find_flights_for_month(city_a.city_code, city_b.city_code, outbound_date.date())
    return build_response([f.to_serializable() for f in sky_scanner_flights])
