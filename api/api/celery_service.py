from commons.backend_service import BackendService
from commons.instagram import InstagramMedia
from commons.logs import get_logger
from commons.sky_scanner import Flight
from commons.uber import UberPricing
from commons.weather import Weather5DayForecast
from executor.tasks import retrieve_weather, retrieve_instagram_media, retrieve_sky_scanner_flights, \
    retrieve_uber_3km_pricing


class CeleryService(BackendService):
    def get_weather_forecast(self, location):
        """
        :type location: commons.model.Location
        :rtype: list[commons.weather.Weather5DayForecast]
        """
        self.logger.info("Retrieving weather for: {}...".format(location))
        try:
            async_result = _run_task(retrieve_weather, location.to_serializable())
            self.logger.info("Sent task {} for weather retrieval!".format(async_result.task_id))
            weather_forecast_serialized = _wait_for_task_and_get_result(async_result)
            self.logger.info("Weather retrieval task {} done!".format(async_result.task_id))
            return [Weather5DayForecast.from_serializable(f) for f in weather_forecast_serialized]
        except Exception as e:
            self.logger.error("Could not retrieve weather for: {}. Details: {}".format(location, e))
            raise e

    def retrieve_instagram_media(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.instagram.InstagramMedia]
        """
        self.logger.info("Retrieving instagram media for: {}...".format(city))
        try:
            async_result = _run_task(retrieve_instagram_media, city.to_serializable())
            self.logger.info("Sent task {} for instagram media retrieval!".format(async_result.task_id))
            instagram_media_serialized = _wait_for_task_and_get_result(async_result)
            self.logger.info("Instagram media retrieval task {} done!".format(async_result.task_id))
            return [InstagramMedia.from_serializable(f) for f in instagram_media_serialized]
        except Exception as e:
            self.logger.error("Could not retrieve instagram media for: {}. Details: {}".format(city, e))
            raise e

    def retrieve_sky_scanner_flights(self, city_a, city_b, outbound_date):
        """
        :type city_a: commons.model.City
        :type city_b: commons.model.City
        :type outbound_date: datetime.date
        :rtype: list[commons.sky_scanner.Flight]
        """
        self.logger.info("Retrieving SkyScanner flights for: {} -> {} on: {}...".format(city_a, city_b, outbound_date))
        try:
            async_result = _run_task(retrieve_sky_scanner_flights, city_a.to_serializable(), city_b.to_serializable(),
                                     outbound_date.isoformat())
            self.logger.info("Sent task {} for SkyScanner flights retrieval!".format(async_result.task_id))
            sky_scanner_flights_serialized = _wait_for_task_and_get_result(async_result)
            self.logger.info("Retrieved SkyScanner flights from task: {}!".format(async_result.task_id))
            return [Flight.from_serializable(f) for f in sky_scanner_flights_serialized]
        except Exception as e:
            self.logger.error("Could not retrieve instagram media for: {} -> {}. Details: {}".format(city_a, city_b, e))
            raise e

    def retrieve_uber_3km_pricing(self, city):
        """
        :type city: commons.model.City
        :rtype: list[commons.uber.UberPricing]
        """
        self.logger.info("Retrieving Uber pricing for 3km from: {}...".format(city))
        try:
            async_result = _run_task(retrieve_uber_3km_pricing, city.location.to_serializable())
            self.logger.info("Sent task {} for Uber pricing retrieval!".format(async_result.task_id))
            uber_pricing_serialized = _wait_for_task_and_get_result(async_result)
            self.logger.info("Retrieved Uber pricing from task: {}!".format(async_result.task_id))
            return [UberPricing.from_serializable(f) for f in uber_pricing_serialized]
        except Exception as e:
            self.logger.error("Could not retrieve Uber pricing for: {}. Details: {}".format(city, e))
            raise e


def _run_task(task, *args):
    """
    Method just to have type checking
    :type task: callable
    :rtype: celery.result.AsyncResult
    """
    return task.delay(*args)


def _wait_for_task_and_get_result(async_result,):
    """
    :type async_result: celery.result.AsyncResult
    :rtype: dict | list | object
    """
    logger = get_logger()
    logger.info("Waiting synchronously for task {} and retuning results...".format(async_result.task_id))
    try:
        return async_result.get()
    except Exception as e:
        logger.error("Error while waiting for result: {}. Details: {}".format(async_result.task_id, e))
        raise e
