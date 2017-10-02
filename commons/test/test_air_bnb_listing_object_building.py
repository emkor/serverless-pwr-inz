import json
import unittest

from commons.air_bnb import build_air_bnb_listing_object
from commons.model import Price, Location

AIR_BNB_RESPONSE = """
      {
      "listing": {
        "bathrooms": 1.0,
        "bedrooms": 1,
        "beds": 2,
        "city": "Ostuni",
        "distance": null,
        "extra_host_languages": [
          "de",
          "en"
        ],
        "id": 432044,
        "instant_bookable": false,
        "is_business_travel_ready": false,
        "is_family_preferred": false,
        "is_new_listing": false,
        "lat": 40.71919290408344,
        "lng": 17.430601156522822,
        "localized_city": "Ostuni",
        "name": "I SETTE CONI - TRULLO EDERA ",
        "neighborhood": null,
        "person_capacity": 4,
        "picture_count": 35,
        "picture_url": "https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg?aki_policy=large",
        "primary_host": {
          "first_name": "Anna",
          "has_profile_pic": true,
          "id": 294274,
          "picture_url": "https://a0.muscache.com/im/users/294274/profile_pic/1333617457/original.jpg?aki_policy=profile_x_medium",
          "smart_name": "Anna",
          "thumbnail_url": "https://a0.muscache.com/im/users/294274/profile_pic/1333617457/original.jpg?aki_policy=profile_small",
          "is_superhost": true
        },
        "property_type": "House",
        "property_type_id": 2,
        "public_address": "Ostuni, Brindisi, Italy",
        "reviews_count": 78,
        "room_type": "Entire home/apt",
        "room_type_category": "entire_home",
        "scrim_color": "#34211B",
        "star_rating": 5.0,
        "thumbnail_url": "https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg?aki_policy=small",
        "user": {
          "first_name": "Anna",
          "has_profile_pic": true,
          "id": 294274,
          "picture_url": "https://a0.muscache.com/im/users/294274/profile_pic/1333617457/original.jpg?aki_policy=profile_x_medium",
          "smart_name": "Anna",
          "thumbnail_url": "https://a0.muscache.com/im/users/294274/profile_pic/1333617457/original.jpg?aki_policy=profile_small",
          "is_superhost": true
        },
        "user_id": 294274,
        "xl_picture_url": "https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg?aki_policy=x_large",
        "preview_encoded_png": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAADCAIAAADUVFKvAAAAO0lEQVQIHQEwAM//AbK+3/b5/+zo5gwQE/v6+QGDd2MKCRnx7O8LCAQjJyYBfG5hCgP29u78CAoBDR0qbvUVieSnXHgAAAAASUVORK5CYII=",
        "picture_urls": [
          "https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273266/24e0c106_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273672/959e6666_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273567/7e9e58c0_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273152/da417cfc_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273197/9007aa3f_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272333/513ff8ec_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273092/150100d1_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273060/4fdd635c_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272420/ef60d3c5_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272510/4d87e5f3_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273012/dadc3627_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272613/5f6cd806_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272987/67eca779_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272945/2b594d85_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273884/81d8e844_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272708/f3dd9530_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272922/5ad7d1b1_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272742/723ca939_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272836/5ce99feb_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272786/f924b311_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15272888/14c47d01_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/60423717/4d68384e_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/15273805/39243fb3_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127147/5ad1df00_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127260/f94a9d80_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127205/0381e543_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/4959132/113114ff_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127265/80e64f8c_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/12208055/31761c97_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127185/e1c600bb_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/4959136/7c704cbb_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/4959142/6a0b1cac_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127157/23118319_original.jpg?aki_policy=large",
          "https://a0.muscache.com/im/pictures/8127332/4380818c_original.jpg?aki_policy=large"
        ],
        "xl_picture_urls": [
          "https://a0.muscache.com/im/pictures/15273358/d7329e9a_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273266/24e0c106_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273672/959e6666_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273567/7e9e58c0_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273152/da417cfc_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273197/9007aa3f_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272333/513ff8ec_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273092/150100d1_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273060/4fdd635c_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272420/ef60d3c5_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272510/4d87e5f3_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273012/dadc3627_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272613/5f6cd806_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272987/67eca779_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272945/2b594d85_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273884/81d8e844_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272708/f3dd9530_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272922/5ad7d1b1_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272742/723ca939_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272836/5ce99feb_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272786/f924b311_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15272888/14c47d01_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/60423717/4d68384e_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/15273805/39243fb3_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127147/5ad1df00_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127260/f94a9d80_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127205/0381e543_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/4959132/113114ff_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127265/80e64f8c_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/12208055/31761c97_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127185/e1c600bb_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/4959136/7c704cbb_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/4959142/6a0b1cac_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127157/23118319_original.jpg?aki_policy=x_large",
          "https://a0.muscache.com/im/pictures/8127332/4380818c_original.jpg?aki_policy=x_large"
        ]
      },
      "pricing_quote": {
        "available": false,
        "checkin": null,
        "checkout": null,
        "guests": 1,
        "guest_details": {
          "number_of_adults": 1,
          "number_of_children": 0,
          "number_of_infants": 0
        },
        "listing_currency": "EUR",
        "localized_currency": "USD",
        "localized_nightly_price": 67,
        "localized_service_fee": 0,
        "localized_total_price": 0,
        "long_term_discount_amount_as_guest": 0,
        "nightly_price": 65,
        "service_fee": 0,
        "total_price": 0
      },
      "viewed_at": null
    }
"""


class TestAirBnbModels(unittest.TestCase):
    def setUp(self):
        self.api_response = json.loads(AIR_BNB_RESPONSE)

    def test_listing_object_building(self):
        actual_object = build_air_bnb_listing_object(self.api_response)
        expected_price = Price(value=67, currency="USD")
        expected_location = Location(latitude=40.71919290408344, longitude=17.430601156522822)
        self.assertIsNotNone(actual_object)
        self.assertEqual(actual_object.location, expected_location)
        self.assertEqual(actual_object.price, expected_price)
