import cherrypy

from api.celery_service import CeleryService
from api.lambda_service import LambdaService
from api.places_import import import_from_file
from api.rest.instagram import InstagramApi
from api.rest.places import PlacesApi
from api.rest.sky_scanner import SkyScannerApi
from api.rest.uber import UberApi
from api.rest.weather import WeatherApi
from commons.api_abstraction import RestApi
from commons.logs import setup_logger, get_logger
from commons.os_utils import get_env_variable

DEFAULT_LAMBDA_SERVICE_URL = ""  # TODO fill with your Lambda service URL
LOG_LEVEL = "INFO"
HTTP_CHERRYPY_CONFIG_FILE = "http_server.conf"
COORDINATOR_API_CONF = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [("Access-Control-Allow-Origin", "*"),
                                           ("Access-Control-Allow-Methods", "GET, POST"),
                                           ("Access-Control-Allow-Headers",
                                            "Content-Type, Cache-Control, X-Proxy-Authorization, X-Requested-With")]
    }
}

if __name__ == '__main__':
    setup_logger(LOG_LEVEL)
    logger = get_logger()
    logger.info("Starting API app...")

    use_aws_lambda = int(get_env_variable("USE_AWS_LAMBDA"))
    if use_aws_lambda:
        aws_lambda_service_url = get_env_variable("AWS_LAMBDA_SERVICE_URL") or DEFAULT_LAMBDA_SERVICE_URL
        service = LambdaService(logger=logger, base_service_url=aws_lambda_service_url)
        logger.info("Initializing API with LambdaService underneath...")
    else:
        service = CeleryService(logger=logger)
        logger.info("Initializing API with CeleryService underneath...")
    places = import_from_file("ServerlessPwrInz-Cities.csv")
    root_api = RestApi(logger=logger)
    root_api.places = PlacesApi(places_list=places, logger=logger)
    root_api.weather = WeatherApi(service=service, places_list=places, logger=logger)
    root_api.instagram = InstagramApi(service=service, places_list=places, logger=logger)
    root_api.skyscanner = SkyScannerApi(service=service, places_list=places, logger=logger)
    root_api.uber = UberApi(service=service, places_list=places, logger=logger)

    cherrypy.log.error_log.propagate = False
    cherrypy.log.access_log.propagate = False
    cherrypy.config.update(HTTP_CHERRYPY_CONFIG_FILE)
    cherrypy.tree.mount(root_api, '/', COORDINATOR_API_CONF)

    logger.info("Starting API...")
    cherrypy.engine.start()
    cherrypy.engine.block()
