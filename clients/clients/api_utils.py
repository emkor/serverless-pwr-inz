from datetime import datetime
from time import sleep

import requests


def keep_polling_when(url, params, status_code_to_poll_on=503, timeout=3, tick=0.5):
    """
    :type url: str
    :type params: dict[str]
    :type status_code_to_poll_on: int
    :type timeout: float
    :type tick: float
    :rtype: requests.Response
    """
    start_time = datetime.utcnow()
    response = None
    while seconds_since(start_time) <= timeout:
        response = requests.get(url=url, params=params)
        if response.status_code == status_code_to_poll_on:
            sleep(tick)
        else:
            return response
    print("Service did not respond after: {}s. Returning response with code: {}".format(seconds_since(start_time),
                                                                                        response.status_code))
    return response


def seconds_since(start_point):
    """
    :type start_point: datetime
    :rtype: float
    """
    return round((datetime.utcnow() - start_point).total_seconds(), 3)
