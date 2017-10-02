import json
import unittest

from commons.instagram import build_instagram_media_object, InstagramLocation, InstagramMedia

INSTAGRAM_OBJECT_RESPONSE = '''
{
      "id": "1508703061085050836_2014123616",
      "user": {
        "id": "2014123616",
        "full_name": "z.bro\u017cek",
        "profile_picture": "https://scontent.cdninstagram.com/t51.2885-19/10254350_201027140241777_810704216_a.jpg",
        "username": "holoreina"
      },
      "images": {
        "thumbnail": {
          "width": 150,
          "height": 150,
          "url": "https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/c0.135.1080.1080/18380457_289035154875217_5161135364923981824_n.jpg"
        },
        "low_resolution": {
          "width": 320,
          "height": 320,
          "url": "https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/c0.135.1080.1080/18380457_289035154875217_5161135364923981824_n.jpg"
        },
        "standard_resolution": {
          "width": 640,
          "height": 640,
          "url": "https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.135.1080.1080/18380457_289035154875217_5161135364923981824_n.jpg"
        }
      },
      "created_time": "1494071441",
      "caption": {
        "id": "17856564394146914",
        "text": "fav Bresalu breakfast place with my girl \u2600\ufe0f\u2615\ufe0f #foodporn #weekend #morning #breakfast #lunch #eggsandbacon #coffee #brunch #lunchdate #wroclaw #friends #foodie #healthy #french #mood #chill #aesthetic #goals #tumblr #poland #salad #breslau #giselle #travel",
        "created_time": "1494071441",
        "from": {
          "id": "2014123616",
          "full_name": "z.bro\u017cek",
          "profile_picture": "https://scontent.cdninstagram.com/t51.2885-19/10254350_201027140241777_810704216_a.jpg",
          "username": "holoreina"
        }
      },
      "user_has_liked": false,
      "likes": {
        "count": 4
      },
      "tags": [
        "morning",
        "tumblr",
        "travel",
        "foodie",
        "healthy",
        "mood",
        "coffee",
        "wroclaw",
        "friends",
        "eggsandbacon",
        "aesthetic",
        "french",
        "goals",
        "salad",
        "lunch",
        "chill",
        "poland",
        "breakfast",
        "giselle",
        "lunchdate",
        "foodporn",
        "brunch",
        "weekend",
        "breslau"
      ],
      "filter": "Normal",
      "comments": {
        "count": 0
      },
      "type": "image",
      "link": "https://www.instagram.com/p/BTv_XDLhNfU/",
      "location": {
        "latitude": 51.11143,
        "longitude": 17.03538,
        "name": "Giselle",
        "id": 63048094
      },
      "attribution": null,
      "users_in_photo": []
    }
'''


class TestBuildingInstagramObjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.json_content = json.loads(INSTAGRAM_OBJECT_RESPONSE)

    def test_should_build_proper_object(self):
        expected_object_location = InstagramLocation(latitude=51.11143,
                                                     longitude=17.03538,
                                                     location_id=63048094,
                                                     location_name=u'Giselle')
        expected_object = InstagramMedia(media_id=u'1508703061085050836_2014123616', location=expected_object_location,
                                         media_type=u'image',
                                         img_url_320=u'https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/c0.135.1080.1080/18380457_289035154875217_5161135364923981824_n.jpg',
                                         img_url_640=u'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.135.1080.1080/18380457_289035154875217_5161135364923981824_n.jpg',
                                         created_timestamp=1494071441, likes_count=4,
                                         tags=[u'morning', u'tumblr', u'travel', u'foodie', u'healthy', u'mood',
                                               u'coffee', u'wroclaw', u'friends',
                                               u'eggsandbacon', u'aesthetic', u'french', u'goals', u'salad', u'lunch',
                                               u'chill', u'poland',
                                               u'breakfast', u'giselle', u'lunchdate', u'foodporn', u'brunch',
                                               u'weekend', u'breslau'])
        actual_object = build_instagram_media_object(self.json_content)
        self.assertEqual(actual_object, expected_object)
