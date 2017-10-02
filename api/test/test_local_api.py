import unittest
import requests
from commons.resources import DEFAULT_CITIES


class CeleryBasedLocalApiTest(unittest.TestCase):
    def setUp(self):
        self.local_api_url = "http://localhost:8080"

    def test_places_api(self):
        places_api_url = "{}/{}".format(self.local_api_url, "places")
        response = requests.get(url=places_api_url)
        self.assertEqual(response.status_code, 200)

        response_content = response.json()
        self.assertTrue(isinstance(response_content, list))
        self.assertGreaterEqual(len(response_content), 1)

    def test_weather_status_api(self):
        self._assert_status_api("weather", 200)

    def test_weather_retrieval_api(self):
        self._assert_retrieval_api("weather", list, 2, 200, 1)

    def test_uber_status_api(self):
        self._assert_status_api("uber", 200)

    def test_uber_pricing_retrieval_api(self):
        self._assert_retrieval_api("uber", list, 1, 200, 1)

    def test_instagram_status_api(self):
        self._assert_status_api("instagram", 200)

    def test_instagram_retrieval_api(self):
        self._assert_retrieval_api("instagram", list, 0, 200, 2)

    def test_sky_scanner_status_api(self):
        self._assert_status_api("skyscanner", 200)

    def test_sky_scanner_flight_retrieval_api(self):
        api_url = "{}/{}".format(self.local_api_url, "skyscanner")
        city_a = DEFAULT_CITIES[1]
        city_b = DEFAULT_CITIES[2]
        response = requests.post(url=api_url,
                                 json={"city_a": city_a.to_serializable(), "city_b": city_b.to_serializable()})
        self.assertEqual(response.status_code, 200)

        response_content = response.json()
        response_type_error_message = "Response type for {} was not {}. Response: {}".format(api_url, str(
            list), response_content)
        response_len_error_message = "Response len() for {} was < {}. Response: {}".format(api_url, 1,
                                                                                           response_content)
        self.assertTrue(isinstance(response_content, list), msg=response_type_error_message)
        self.assertGreaterEqual(len(response_content), 1, msg=response_len_error_message)

    def _assert_retrieval_api(self, sub_url, expected_response_type, requested_city_id=0, expected_status_code=200,
                              min_response_length=1):
        """
        :type sub_url: str
        :type expected_response_type: class
        :type requested_city_id: int
        :type expected_status_code: int
        :type min_response_length: int
        """
        api_url = "{}/{}".format(self.local_api_url, sub_url)
        city = DEFAULT_CITIES[requested_city_id]
        response = requests.post(url=api_url, json=city.to_serializable())
        response_code_error_message = "Response code for {} was: {}. Response: {}".format(api_url, response.status_code,
                                                                                          response.content)
        self.assertEqual(response.status_code, expected_status_code, response_code_error_message)

        response_content = response.json()
        response_type_error_message = "Response type for {} was not {}. Response: {}".format(api_url, str(
            expected_response_type), response_content)
        response_len_error_message = "Response len() for {} was < {}. Response: {}".format(api_url, min_response_length,
                                                                                           response_content)
        self.assertTrue(isinstance(response_content, expected_response_type), msg=response_type_error_message)
        self.assertGreaterEqual(len(response_content), min_response_length, msg=response_len_error_message)

    def _assert_status_api(self, sub_url, expected_status_code=200):
        """
        :type sub_url: str
        :type expected_status_code: int
        """
        response = requests.get(url="{}/{}".format(self.local_api_url, sub_url))
        self.assertEqual(response.status_code, expected_status_code)
