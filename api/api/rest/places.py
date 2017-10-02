from commons.api_abstraction import RestApi


class PlacesApi(RestApi):
    def __init__(self, places_list, logger=None):
        """
        :type places_list: list[commons.model.City]
        :type logger: logging.Logger
        """
        super(PlacesApi, self).__init__(logger)
        self.places_list = places_list

    def get(self, request_url, query_params):
        if not query_params:
            return self.places_list
        city_name = query_params.get("city_name")
        return filter(lambda p: p.city_name == city_name, self.places_list)

    def put(self, request_url, query_params, request_payload):
        super(PlacesApi, self).put(request_url, query_params)

    def delete(self, request_url, query_params):
        super(PlacesApi, self).delete(request_url, query_params)

    def post(self, request_url, query_params, request_payload):
        super(PlacesApi, self).post(request_url, query_params)
