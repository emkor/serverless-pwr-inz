import requests
from datetime import date

from commons.conversion import normalize
from commons.logs import get_logger
from commons.os_utils import get_env_variable
from commons.sky_scanner import build_flight_query_results

SKY_SCANNER_API_KEY_ENV_NAME = "SKY_SCANNER_API_KEY"
SKY_SCANNER_SERVICE_URL = "http://partners.api.skyscanner.net/apiservices/"
SKY_SCANNER_BROWSE_DATES_SUB_URL = "browsedates/v1.0/"
SKY_SCANNER_LIST_PLACE_CODES = "autosuggest/v1.0/"
SKY_SCANNER_HEADER = {"Content-Type": "application/json"}


def build_sky_scanner_client_from_env_vars():
    """
    :rtype: clients.sky_scanner.SkyScannerClient
    """
    sky_scanner_api_key = get_env_variable(SKY_SCANNER_API_KEY_ENV_NAME)
    return SkyScannerClient(api_key=sky_scanner_api_key, market="PL", locale="en-GB", currency="USD")


def _prepare_date_format(date_for_month):
    """
    :type date_for_month: date
    :rtype: str
    """
    return str(date_for_month)[:-3]


class SkyScannerClient(object):
    def __init__(self, api_key, market, locale, currency):
        """
        :type api_key: str
        :param market: The users market country, Skyscanner country code
        :type market: str
        :param locale: The users selected language, ISO locale code
        :type locale: str
        :param currency: The users selected currency, ISO currency code
        :type currency: str
        """
        self.api_key = api_key
        self.locale = locale
        self.market = market
        self.currency = currency
        self.logger = get_logger()

    def find_flights_for_month(self, start_city, end_city, outbound_date):
        """
        :type start_city: str
        :type end_city: str
        :type outbound_date: datetime.date
        :rtype: list[commons.sky_scanner.Flight]
        """
        outbound_date_str = _prepare_date_format(outbound_date)
        query_url = "{}/{}/{}/{}/{}/{}?apiKey={}".format(self.market, self.currency, self.locale,
                                                         start_city, end_city, outbound_date_str,
                                                         self.api_key)
        full_url = SKY_SCANNER_SERVICE_URL + SKY_SCANNER_BROWSE_DATES_SUB_URL + query_url
        self.logger.info("Retrieving flights from sky scanner using url: {}...".format(full_url))
        response = requests.get(url=full_url, headers=SKY_SCANNER_HEADER)
        if response.ok:
            return build_flight_query_results(response.json())
        else:
            raise IOError("Error response from SkyScanner API. Code: {} content: {}".format(response.status_code,
                                                                                            response.content))
