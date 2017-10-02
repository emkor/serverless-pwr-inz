import calendar
from datetime import datetime
from math import cos, sqrt, radians, sin, asin
from unidecode import unidecode
from dateutil.parser import parse
from commons.model import Price

_USD_CURRENCY_CONVERSION_RATES = {"AUD": 1.3545, "BGN": 1.7973, "BRL": 3.1649, "CAD": 1.3697, "CHF": 1.0062,
                                  "CNY": 6.9028, "CZK": 24.483, "DKK": 6.8378, "GBP": 0.77178, "HKD": 7.7861,
                                  "HRK": 6.82, "HUF": 285.42, "IDR": 13358.0, "ILS": 3.6007, "INR": 64.546,
                                  "JPY": 113.8, "KRW": 1134.9, "MXN": 19.075, "MYR": 4.347, "NOK": 8.6781,
                                  "NZD": 1.4401, "PHP": 49.912, "PLN": 3.8761, "RON": 4.1808, "RUB": 57.856,
                                  "SEK": 8.9129, "SGD": 1.4104, "THB": 34.76, "TRY": 3.5891, "ZAR": 13.49,
                                  "EUR": 0.91895}


def convert_price(price, target_currency):
    """
    :type price: commons.model.Price
    :type target_currency: target_currency
    :rtype: commons.model.Price
    """
    if normalize(price.currency) == normalize(target_currency):
        return price
    elif normalize(price.currency) == normalize("USD"):
        return Price(currency=target_currency,
                     value=price.value * _USD_CURRENCY_CONVERSION_RATES.get(target_currency) or 1)
    elif normalize(target_currency) == normalize("USD"):
        return Price(currency=target_currency,
                     value=price.value / _USD_CURRENCY_CONVERSION_RATES.get(price.currency) or 1)
    else:
        usd_price = convert_price(price=price, target_currency="USD")
        return convert_price(usd_price, target_currency)


def utc_datetime_to_timestamp(dt):
    """
    Converts datetime (UTC) to Unix timestamp
    :type dt: datetime
    :rtype: int
    """
    return calendar.timegm(dt.utctimetuple())


def utc_timestamp_to_datetime(timestamp):
    """
    Converts timestamp (seconds) to UTC datetime
    :type timestamp: float | int
    :rtype: datetime
    """
    return datetime.utcfromtimestamp(round(timestamp))


def normalize(text):
    """
    :type text: str | unicode
    :rtype: str
    """
    if isinstance(text, str):
        return text.strip().lower()
    elif isinstance(text, unicode):
        return unidecode(text.strip()).lower()


def distance(location_a, location_b):
    """
    Returns distance between locations in km
    :type location_a: commons.model.Location
    :type location_b: commons.model.Location
    :rtype: float
    """
    lon1, lat1, lon2, lat2 = map(radians, [location_a.longitude, location_a.latitude,
                                           location_b.longitude, location_b.latitude])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6367 * 2 * asin(sqrt(a))


def parse_date(date_string):
    """
    :type date_string: str
    :rtype: datetime
    """
    return parse(date_string)
