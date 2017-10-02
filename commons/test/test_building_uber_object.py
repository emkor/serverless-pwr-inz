from commons.model import Price
from commons.uber import UberProduct, build_uber_product_object, build_uber_pricing_object, UberPricing
import json
import unittest

UBER_PRODUCT_RESPONSE = """
{
      "upfront_fare_enabled": false,
      "capacity": 4,
      "product_id": "2bc02557-7c84-4a21-88bd-261dd5b3a816",
      "price_details": {
        "distance_unit": "km",
        "cost_per_minute": 0.25,
        "service_fees": [],
        "minimum": 10.0,
        "cost_per_distance": 1.3,
        "base": 4.0,
        "cancellation_fee": 10.0,
        "currency_code": "PLN"
      },
      "image": "http://d1a3f4spazzrp4.cloudfront.net/car-types/mono/mono-uberx.png",
      "description": "THE LOW-COST UBER",
      "cash_enabled": false,
      "short_description": "uberPOP",
      "shared": false,
      "product_group": "uberx",
      "display_name": "uberPOP"
    }
"""

UBER_PRICING_RESPONSE = """
{
    "localized_display_name": "uberPOP",
    "distance": 1.67,
    "display_name": "uberPOP",
    "product_id": "2bc02557-7c84-4a21-88bd-261dd5b3a816",
    "high_estimate": 12.0,
    "duration": 660,
    "minimum": 10,
    "low_estimate": 10.0,
    "surge_multiplier": 1.0,
    "estimate": "PLN10-12",
    "currency_code": "PLN"
}
"""


class TestUberClient(unittest.TestCase):
    def setUp(self):
        self.product_json_response = json.loads(UBER_PRODUCT_RESPONSE)
        self.pricing_json_response = json.loads(UBER_PRICING_RESPONSE)

    def test_should_build_product_object_from_uber_response(self):
        expected_object = UberProduct(id="2bc02557-7c84-4a21-88bd-261dd5b3a816", name="uberPOP",
                                      description="THE LOW-COST UBER", capacity=4)
        actual_object = build_uber_product_object(self.product_json_response)
        self.assertIsNotNone(actual_object)
        self.assertEqual(expected_object, actual_object)

    def test_should_build_pricing_object_from_uber_response(self):
        expected_object = UberPricing(product_id="2bc02557-7c84-4a21-88bd-261dd5b3a816", product_name="uberPOP",
                                      duration=660, distance=1.67,
                                      low_estimate=Price(10, "PLN"),
                                      high_estimate=Price(12, "PLN"))
        actual_object = build_uber_pricing_object(self.pricing_json_response)
        self.assertIsNotNone(actual_object)
        self.assertEqual(expected_object, actual_object)
