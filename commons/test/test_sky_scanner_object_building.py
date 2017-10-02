import json
import unittest

from commons.sky_scanner import build_flight_query_results

SKY_SCANNER_EXAMPLE_RESPONSE = """
{
  "Dates": {
    "OutboundDates": [
      {
        "PartialDate": "2017-06-01",
        "QuoteIds": [
          1,
          2,
          3,
          4
        ],
        "Price": 46.0,
        "QuoteDateTime": "2017-05-08T07:57:46"
      },
      {
        "PartialDate": "2017-06-02",
        "QuoteIds": [
          5,
          6,
          7,
          8,
          9
        ],
        "Price": 71.0,
        "QuoteDateTime": "2017-05-09T13:09:42"
      },
      {
        "PartialDate": "2017-06-03",
        "QuoteIds": [
          10,
          11,
          12,
          13
        ],
        "Price": 121.0,
        "QuoteDateTime": "2017-05-09T13:29:04"
      }
    ]
  },
  "Quotes": [
    {
      "QuoteId": 1,
      "MinPrice": 76.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          881
        ],
        "OriginId": 84892,
        "DestinationId": 65465,
        "DepartureDate": "2017-06-01T00:00:00"
      },
      "QuoteDateTime": "2017-05-09T13:14:25"
    },
    {
      "QuoteId": 2,
      "MinPrice": 50.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 66270,
        "DepartureDate": "2017-06-01T00:00:00"
      },
      "QuoteDateTime": "2017-05-08T07:57:46"
    },
    {
      "QuoteId": 3,
      "MinPrice": 77.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1047
        ],
        "OriginId": 84892,
        "DestinationId": 65698,
        "DepartureDate": "2017-06-01T00:00:00"
      },
      "QuoteDateTime": "2017-05-12T05:38:53"
    },
    {
      "QuoteId": 4,
      "MinPrice": 46.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 65655,
        "DepartureDate": "2017-06-01T00:00:00"
      },
      "QuoteDateTime": "2017-05-08T07:57:46"
    },
    {
      "QuoteId": 5,
      "MinPrice": 153.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          881
        ],
        "OriginId": 84892,
        "DestinationId": 65465,
        "DepartureDate": "2017-06-02T00:00:00"
      },
      "QuoteDateTime": "2017-05-11T23:33:13"
    },
    {
      "QuoteId": 6,
      "MinPrice": 71.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 66270,
        "DepartureDate": "2017-06-02T00:00:00"
      },
      "QuoteDateTime": "2017-05-09T13:09:42"
    },
    {
      "QuoteId": 7,
      "MinPrice": 161.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          881
        ],
        "OriginId": 84892,
        "DestinationId": 82398,
        "DepartureDate": "2017-06-02T00:00:00"
      },
      "QuoteDateTime": "2017-05-11T23:33:13"
    },
    {
      "QuoteId": 8,
      "MinPrice": 155.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1047
        ],
        "OriginId": 84892,
        "DestinationId": 65698,
        "DepartureDate": "2017-06-02T00:00:00"
      },
      "QuoteDateTime": "2017-05-12T07:25:29"
    },
    {
      "QuoteId": 9,
      "MinPrice": 97.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 65655,
        "DepartureDate": "2017-06-02T00:00:00"
      },
      "QuoteDateTime": "2017-05-09T13:09:42"
    },
    {
      "QuoteId": 10,
      "MinPrice": 145.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 66270,
        "DepartureDate": "2017-06-03T00:00:00"
      },
      "QuoteDateTime": "2017-05-11T23:02:29"
    },
    {
      "QuoteId": 11,
      "MinPrice": 121.0,
      "Direct": false,
      "OutboundLeg": {
        "CarrierIds": [
          1047
        ],
        "OriginId": 84892,
        "DestinationId": 65698,
        "DepartureDate": "2017-06-03T00:00:00"
      },
      "QuoteDateTime": "2017-05-09T18:33:18"
    },
    {
      "QuoteId": 12,
      "MinPrice": 194.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1047
        ],
        "OriginId": 84892,
        "DestinationId": 65698,
        "DepartureDate": "2017-06-03T00:00:00"
      },
      "QuoteDateTime": "2017-05-12T07:25:29"
    },
    {
      "QuoteId": 13,
      "MinPrice": 139.0,
      "Direct": true,
      "OutboundLeg": {
        "CarrierIds": [
          1050
        ],
        "OriginId": 82582,
        "DestinationId": 65655,
        "DepartureDate": "2017-06-03T00:00:00"
      },
      "QuoteDateTime": "2017-05-09T13:29:04"
    }
  ],
  "Places": [
    {
      "PlaceId": 65465,
      "IataCode": "LCY",
      "Name": "London City",
      "Type": "Station",
      "SkyscannerCode": "LCY",
      "CityName": "London",
      "CityId": "LOND",
      "CountryName": "United Kingdom"
    },
    {
      "PlaceId": 65655,
      "IataCode": "LGW",
      "Name": "London Gatwick",
      "Type": "Station",
      "SkyscannerCode": "LGW",
      "CityName": "London",
      "CityId": "LOND",
      "CountryName": "United Kingdom"
    },
    {
      "PlaceId": 65698,
      "IataCode": "LHR",
      "Name": "London Heathrow",
      "Type": "Station",
      "SkyscannerCode": "LHR",
      "CityName": "London",
      "CityId": "LOND",
      "CountryName": "United Kingdom"
    },
    {
      "PlaceId": 66270,
      "IataCode": "LTN",
      "Name": "London Luton",
      "Type": "Station",
      "SkyscannerCode": "LTN",
      "CityName": "London",
      "CityId": "LOND",
      "CountryName": "United Kingdom"
    },
    {
      "PlaceId": 82398,
      "IataCode": "STN",
      "Name": "London Stansted",
      "Type": "Station",
      "SkyscannerCode": "STN",
      "CityName": "London",
      "CityId": "LOND",
      "CountryName": "United Kingdom"
    },
    {
      "PlaceId": 82582,
      "IataCode": "SXF",
      "Name": "Berlin Schoenefeld",
      "Type": "Station",
      "SkyscannerCode": "SXF",
      "CityName": "Berlin",
      "CityId": "BERL",
      "CountryName": "Germany"
    },
    {
      "PlaceId": 84892,
      "IataCode": "TXL",
      "Name": "Berlin Tegel",
      "Type": "Station",
      "SkyscannerCode": "TXL",
      "CityName": "Berlin",
      "CityId": "BERL",
      "CountryName": "Germany"
    }
  ],
  "Carriers": [
    {
      "CarrierId": 881,
      "Name": "British Airways"
    },
    {
      "CarrierId": 885,
      "Name": "Flybe"
    },
    {
      "CarrierId": 1001,
      "Name": "Norwegian"
    },
    {
      "CarrierId": 1047,
      "Name": "eurowings"
    },
    {
      "CarrierId": 1050,
      "Name": "easyJet"
    },
    {
      "CarrierId": 1710,
      "Name": "Brussels Airlines"
    },
    {
      "CarrierId": 1914,
      "Name": "Wizz Air"
    }
  ],
  "Currencies": [
    {
      "Code": "USD",
      "Symbol": "$",
      "ThousandsSeparator": ",",
      "DecimalSeparator": ".",
      "SymbolOnLeft": true,
      "SpaceBetweenAmountAndSymbol": false,
      "RoundingCoefficient": 0,
      "DecimalDigits": 2
    }
  ]
}
"""

SKY_SCANNER_PROBLEMATIC_RESPONSE = {u'Quotes':
                                        [{u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                           u'OriginId': 84892,
                                                           u'DepartureDate': u'2017-06-15T00:00:00'},
                                          u'MinPrice': 158.0, u'QuoteId': 1, u'Direct': False,
                                          u'QuoteDateTime': u'2017-06-14T05:48:38'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-16T00:00:00'},
                                             u'MinPrice': 166.0, u'QuoteId': 2, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T07:51:39'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-16T00:00:00'},
                                             u'MinPrice': 149.0, u'QuoteId': 3, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T05:37:46'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-17T00:00:00'},
                                             u'MinPrice': 153.0, u'QuoteId': 4, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T07:57:24'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-17T00:00:00'},
                                             u'MinPrice': 149.0, u'QuoteId': 5, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T06:46:34'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-18T00:00:00'},
                                             u'MinPrice': 204.0, u'QuoteId': 6, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-13T10:13:49'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-18T00:00:00'},
                                             u'MinPrice': 158.0, u'QuoteId': 7, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T07:43:55'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-20T00:00:00'},
                                             u'MinPrice': 149.0, u'QuoteId': 8, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T06:39:25'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-21T00:00:00'},
                                             u'MinPrice': 112.0, u'QuoteId': 9, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T05:14:45'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-21T00:00:00'},
                                             u'MinPrice': 149.0, u'QuoteId': 10, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-13T11:23:33'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-22T00:00:00'},
                                             u'MinPrice': 105.0, u'QuoteId': 11, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-04T09:02:27'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1368], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-22T00:00:00'},
                                             u'MinPrice': 149.0, u'QuoteId': 12, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-14T05:17:43'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-23T00:00:00'},
                                             u'MinPrice': 114.0, u'QuoteId': 13, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-04T23:14:58'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1710], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-23T00:00:00'},
                                             u'MinPrice': 133.0, u'QuoteId': 14, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-04T23:14:57'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-24T00:00:00'},
                                             u'MinPrice': 129.0, u'QuoteId': 15, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-09T09:02:44'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-24T00:00:00'},
                                             u'MinPrice': 113.0, u'QuoteId': 16, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-13T11:46:47'}, {
                                             u'OutboundLeg': {u'CarrierIds': [], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-25T00:00:00'},
                                             u'MinPrice': 156.0, u'QuoteId': 17, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T23:24:31'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-25T00:00:00'},
                                             u'MinPrice': 117.0, u'QuoteId': 18, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T23:24:26'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-26T00:00:00'},
                                             u'MinPrice': 117.0, u'QuoteId': 19, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T23:21:20'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-26T00:00:00'},
                                             u'MinPrice': 112.0, u'QuoteId': 20, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T23:21:21'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-27T00:00:00'},
                                             u'MinPrice': 104.0, u'QuoteId': 21, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T14:53:55'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-27T00:00:00'},
                                             u'MinPrice': 117.0, u'QuoteId': 22, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-12T14:53:53'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-28T00:00:00'},
                                             u'MinPrice': 106.0, u'QuoteId': 23, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-09T20:37:58'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-29T00:00:00'},
                                             u'MinPrice': 112.0, u'QuoteId': 24, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-09T20:38:11'}, {
                                             u'OutboundLeg': {u'CarrierIds': [1050], u'DestinationId': 56141,
                                                              u'OriginId': 82582,
                                                              u'DepartureDate': u'2017-06-30T00:00:00'},
                                             u'MinPrice': 110.0, u'QuoteId': 25, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-07T09:34:23'}, {
                                             u'OutboundLeg': {u'CarrierIds': [834], u'DestinationId': 56141,
                                                              u'OriginId': 84892,
                                                              u'DepartureDate': u'2017-06-30T00:00:00'},
                                             u'MinPrice': 122.0, u'QuoteId': 26, u'Direct': False,
                                             u'QuoteDateTime': u'2017-06-07T09:34:23'}], u'Dates': {
    u'OutboundDates': [
        {u'QuoteIds': [1], u'PartialDate': u'2017-06-15', u'Price': 158.0, u'QuoteDateTime': u'2017-06-14T05:48:38'},
        {u'QuoteIds': [2, 3], u'PartialDate': u'2017-06-16', u'Price': 149.0, u'QuoteDateTime': u'2017-06-14T05:37:46'},
        {u'QuoteIds': [4, 5], u'PartialDate': u'2017-06-17', u'Price': 149.0, u'QuoteDateTime': u'2017-06-14T06:46:34'},
        {u'QuoteIds': [6, 7], u'PartialDate': u'2017-06-18', u'Price': 158.0, u'QuoteDateTime': u'2017-06-13T10:13:49'},
        {u'QuoteIds': [8], u'PartialDate': u'2017-06-20', u'Price': 149.0, u'QuoteDateTime': u'2017-06-14T06:39:25'},
        {u'QuoteIds': [9, 10], u'PartialDate': u'2017-06-21', u'Price': 112.0,
         u'QuoteDateTime': u'2017-06-12T05:14:45'},
        {u'QuoteIds': [11, 12], u'PartialDate': u'2017-06-22', u'Price': 105.0,
         u'QuoteDateTime': u'2017-06-04T09:02:27'},
        {u'QuoteIds': [13, 14], u'PartialDate': u'2017-06-23', u'Price': 114.0,
         u'QuoteDateTime': u'2017-06-04T23:14:57'},
        {u'QuoteIds': [15, 16], u'PartialDate': u'2017-06-24', u'Price': 113.0,
         u'QuoteDateTime': u'2017-06-09T09:02:44'},
        {u'QuoteIds': [17, 18], u'PartialDate': u'2017-06-25', u'Price': 117.0,
         u'QuoteDateTime': u'2017-06-12T23:24:26'},
        {u'QuoteIds': [19, 20], u'PartialDate': u'2017-06-26', u'Price': 112.0,
         u'QuoteDateTime': u'2017-06-12T23:21:20'},
        {u'QuoteIds': [21, 22], u'PartialDate': u'2017-06-27', u'Price': 104.0,
         u'QuoteDateTime': u'2017-06-12T14:53:53'},
        {u'QuoteIds': [23], u'PartialDate': u'2017-06-28', u'Price': 106.0, u'QuoteDateTime': u'2017-06-09T20:37:58'},
        {u'QuoteIds': [24], u'PartialDate': u'2017-06-29', u'Price': 112.0, u'QuoteDateTime': u'2017-06-09T20:38:11'},
        {u'QuoteIds': [25, 26], u'PartialDate': u'2017-06-30', u'Price': 110.0,
         u'QuoteDateTime': u'2017-06-07T09:34:23'}]}, u'Currencies': [
    {u'SpaceBetweenAmountAndSymbol': False, u'Code': u'USD', u'SymbolOnLeft': True, u'DecimalSeparator': u'.',
     u'Symbol': u'$', u'ThousandsSeparator': u',', u'RoundingCoefficient': 0, u'DecimalDigits': 2}], u'Places': [
    {u'CountryName': u'Germany', u'Name': u'Hamburg International', u'CityName': u'Hamburg', u'SkyscannerCode': u'HAM',
     u'IataCode': u'HAM', u'PlaceId': 56141, u'CityId': u'HAMB', u'Type': u'Station'},
    {u'CountryName': u'Germany', u'Name': u'Berlin Schoenefeld', u'CityName': u'Berlin', u'SkyscannerCode': u'SXF',
     u'IataCode': u'SXF', u'PlaceId': 82582, u'CityId': u'BERL', u'Type': u'Station'},
    {u'CountryName': u'Germany', u'Name': u'Berlin Tegel', u'CityName': u'Berlin', u'SkyscannerCode': u'TXL',
     u'IataCode': u'TXL', u'PlaceId': 84892, u'CityId': u'BERL', u'Type': u'Station'}],
                                    u'Carriers': [{u'CarrierId': 834, u'Name': u'Air Berlin'},
                                                  {u'CarrierId': 1050, u'Name': u'easyJet'},
                                                  {u'CarrierId': 1368, u'Name': u'Lufthansa'},
                                                  {u'CarrierId': 1710, u'Name': u'Brussels Airlines'}]}


class TestSkyScannerObjectBuilding(unittest.TestCase):
    def setUp(self):
        self.example_response = json.loads(SKY_SCANNER_EXAMPLE_RESPONSE)

    # def test_sky_scanner_flight_response_building(self):
    #     actual_object = build_flight_query_results(api_response_dict=self.example_response)
    #     self.assertIsNotNone(actual_object)
    #     self.assertEqual(13, len(actual_object))

    def test_sky_scanner_flight_problematic_response_building(self):
        actual_object = build_flight_query_results(api_response_dict=SKY_SCANNER_PROBLEMATIC_RESPONSE)
        self.assertIsNotNone(actual_object)
