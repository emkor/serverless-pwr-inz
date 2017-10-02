import cherrypy

from commons.logs import get_logger
from commons.serialization import to_json


class RestApi(object):
    exposed = True

    def __init__(self, logger=None):
        """
        :type logger: logging.Logger
        """
        self.not_implemented_api_method = cherrypy.HTTPError(405, 'Method Not Allowed')
        self.logger = logger or get_logger()

    def get(self, request_url, query_params):
        """
        :type request_url: str
        :type query_params: dict[str, str]
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    def post(self, request_url, query_params, request_payload):
        """
        :type request_url: str
        :type query_params: dict
        :type request_payload: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        """
        :type request_url: str
        :type query_params: dict
        :type request_payload: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        """
        :type request_url: str
        :type query_params: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **query_params):
        request_url = cherrypy.url()
        try:
            response_json = to_json(self.get(request_url=request_url, query_params=query_params))
            self._log_api_call("GET", request_url, response_json)
            return response_json
        except Exception as e:
            self.logger.exception(e)
            raise cherrypy.HTTPError(500, e)

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_in()
    def POST(self, **query_params):
        request_url = cherrypy.url()
        request_json = cherrypy.request.json
        try:
            response_json = to_json(
                self.post(request_url=request_url, query_params=query_params, request_payload=request_json))
            self._log_api_call("POST", request_url, response_json, request_json)
            return response_json
        except Exception as e:
            self.logger.exception(e)
            raise cherrypy.HTTPError(500, e)

    @cherrypy.tools.accept(media='application/json')
    def PUT(self, **query_params):
        request_url = cherrypy.url()
        request_json = cherrypy.request.json
        try:
            response_json = to_json(
                self.post(request_url=request_url, query_params=query_params, request_payload=request_json))
            self._log_api_call("PUT", request_url, response_json, request_json)
            return response_json
        except Exception as e:
            self.logger.exception(e)
            raise cherrypy.HTTPError(500, e)

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, **query_params):
        request_url = cherrypy.url()
        try:
            response_json = to_json(self.delete(request_url=request_url, query_params=query_params))
            self._log_api_call("DELETE", request_url, response_json)
            return response_json
        except Exception as e:
            self.logger.exception(e)
            raise cherrypy.HTTPError(500, e)

    def OPTIONS(self, *args, **kwargs):
        return

    def _log_api_call(self, method_name, request_url, response_json, request_json=None):
        """
        :type method_name: str
        :type request_url: str
        :type response_json: str
        :type request_json: str
        """
        request_len = len(request_json) if request_json else 0
        response_len = len(response_json) if response_json else 0
        self.logger.info(
            "{} on {} at {} with payload {} chars and response {} chars".format(method_name, self.__class__.__name__,
                                                                                request_url, request_len, response_len))
