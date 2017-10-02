import unittest

from commons.model import Location
from commons.serialization import to_json, from_json


class SerializationTest(unittest.TestCase):
    def setUp(self):
        self.location = Location(10.01, -31.16)

    def test_should_serialize_location_object(self):
        serialized_location = to_json(self.location)
        self.assertIsNotNone(serialized_location)

    def test_should_serialize_and_deserialize_location_object(self):
        serialized_location = to_json(self.location)
        deserialized_location = from_json(serialized_location, Location)
        self.assertIsNotNone(deserialized_location)
        self.assertEqual(self.location, deserialized_location)

    def test_model_should_return_serializable(self):
        serializable = self.location.to_serializable()
        self.assertIsNotNone(serializable)
        self.assertEqual(serializable, {"latitude": 10.01, "longitude": -31.16})

    def test_model_should_recreate_object_from_serializable(self):
        serializable = self.location.to_serializable()
        recreated = Location.from_serializable(serializable)
        self.assertIsNotNone(recreated)
        self.assertEqual(self.location, recreated)
