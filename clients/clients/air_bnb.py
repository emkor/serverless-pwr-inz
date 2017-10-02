from clients.api_utils import keep_polling_when
from commons.air_bnb import build_air_bnb_listing_object
from commons.os_utils import get_env_variable

AIR_BNB_CLIENT_ID_ENV_VAR_NAME = "AIR_BNB_CLIENT_ID"
AIR_BNB_SEARCH_ENDPOINT = "https://api.airbnb.com/v2/search_results"


def build_air_bnb_client_using_env_vars():
    """
    :rtype: clients.air_bnb.AirBnbClient
    """
    client_id = get_env_variable(AIR_BNB_CLIENT_ID_ENV_VAR_NAME)
    return AirBnbClient(client_id=client_id, locale="en-US", currency="USD")


class ApiMisbehavesException(Exception):
    pass


class AirBnbClient(object):
    def __init__(self, client_id, locale, currency):
        """
        :type client_id: str
        """
        self.locale = locale
        self.currency = currency
        self.client_id = client_id

    def list_hosts(self, location):
        """
        :type location: commons.model.Location
        :rtype: dict[str]
        """
        url_query_params = {"client_id": self.client_id, "locale": self.locale, "currency": self.currency,
                            "user_lat": location.latitude, "user_lng": location.longitude}

        api_response = keep_polling_when(url=AIR_BNB_SEARCH_ENDPOINT,
                                         params=url_query_params, status_code_to_poll_on=503)
        if api_response.ok:
            search_listing_list = api_response.json().get("search_results")
            listing_objects = [build_air_bnb_listing_object(l) for l in search_listing_list]
            return listing_objects
        elif api_response.status_code == 503:
            raise ApiMisbehavesException(
                "AirBnB API has problems. Status code: {} error content: {}".format(api_response.status_code,
                                                                                    api_response.content))
        else:
            raise IOError(
                "Could not retrieve information from AirBnB API. Code: {} content: {}".format(api_response.status_code,
                                                                                              api_response.content))
