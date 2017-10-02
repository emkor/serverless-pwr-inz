import requests

from commons.conversion import normalize, distance
from commons.instagram import build_instagram_media_object
from commons.logs import get_logger
from commons.os_utils import get_env_variable

INSTAGRAM_CLIENT_ID_ENV_NAME = "INSTAGRAM_CLIENT_ID"
INSTAGRAM_ACCESS_TOKEN_ENV_NAME = "INSTAGRAM_ACCESS_TOKEN"

MAX_ITERATIONS = 3
ALLOWED_MEDIA_FROM_CITY_DISTANCE = 150.
DEFAULT_EXCLUDED_TAGS = ["selfie", "mirror", "me", "myself", "instagirl", "instaboy", "girl", "boy", "girls", "boys",
                         "friend", "friends", "likeforlike", "followforfollow", "like", "follow", "likeit", "followme",
                         "snapback", "instafollow", "dog", "concert", "motorcycle", "motorbike", "streetwear",
                         "politik", "band", "marketing", "ad", "entrepreneur", "business", "sales", "ecommerce",
                         "onlineshopping", "coffee", "power", "sport", "swag", "yolo", "healthyfood", "sale",
                         "bestdeal", "veganfood", "yummy", "heresmyfood", "food", "mcfit", "gayman", "gay", "fitness",
                         "pug", "dogoftheday", "blonde", "instagrammodel", "fashionista", "shooting", "style",
                         "fashionmodel", "model", "fashionblogger", "livemusic", "acoustic", "lads", "mates", "makeup",
                         "like4like"]


def build_instagram_client_using_env_variables(client_id_variable_name=INSTAGRAM_CLIENT_ID_ENV_NAME,
                                               access_token_variable_name=INSTAGRAM_ACCESS_TOKEN_ENV_NAME):
    client_id = get_env_variable(client_id_variable_name, "")
    access_token = get_env_variable(access_token_variable_name, "")
    return InstagramClient(client_id=client_id, access_token=access_token, logger=get_logger())


class InstagramClient(object):
    def __init__(self, client_id, access_token, logger):
        """
        :type client_id: str
        :type access_token: str
        :type logger: logging.Logger
        """
        self.client_id = client_id
        self.access_token = access_token
        self.logger = logger

    def recent_photos_from(self, city, at_least=8, exclude_tags=DEFAULT_EXCLUDED_TAGS):
        """
        :type city: commons.model.City
        :type at_least: int
        :type exclude_tags: list[str]
        :rtype: list[commons.instagram.InstagramMedia]
        """
        normalized_tag = normalize(city.city_name)
        first_url = "https://api.instagram.com/v1/tags/{}/media/recent?access_token={}".format(normalized_tag,
                                                                                               self.access_token)
        iteration, resolved_media_list, next_url = 1, [], first_url
        while len(resolved_media_list) < at_least and iteration <= MAX_ITERATIONS:
            try:
                new_media_list, next_url = self._call_for_content(next_url, exclude_tags, iteration, city)
                resolved_media_list.extend(new_media_list)
            except Exception as e:
                self.logger.error("Error on retrieving Instagram media: {}. Returning {} elements...".format(e, len(
                    resolved_media_list)))
                break
            iteration += 1
        return resolved_media_list

    def _call_for_content(self, url, exclude_tags, iteration, city):
        """
        :type url: str
        :type exclude_tags: list[str]
        :type iteration: int
        :type city: commons.model.City
        :rtype: list[commons.instagram.InstagramMedia]
        """
        self.logger.info(
            "Instagram client calls recent_photos_tagged for {}. time with url: {}...".format(iteration, url))
        r = requests.get(url)
        if r.ok:
            json_response = r.json()
            next_url = json_response.get("pagination").get("next_url")
            media_list = map(lambda media_dict: build_instagram_media_object(media_dict), json_response.get("data"))
            return self._filter_media_list(media_list, exclude_tags, city), next_url
        else:
            raise IOError(
                "Could not retrieve information from Instagram API. Code: {} content: {}".format(r.status_code,
                                                                                                 r.content))

    def _filter_media_list(self, media_list, excluded_tags, city):
        """
        :type media_list: list[commons.instagram.InstagramMedia]
        :type excluded_tags: list[str]
        :type city: commons.model.City
        :rtype: list[commons.instagram.InstagramMedia]
        """
        initial_len = len(media_list)
        filtered_media = filter(
            lambda m: m.is_image()
                      and m.location is not None
                      and distance(m.location, city.location) < ALLOWED_MEDIA_FROM_CITY_DISTANCE
                      and not any([tag in excluded_tags for tag in m.tags]),
            media_list)
        output_len = len(filtered_media)
        self.logger.info("Filtered media: {}/{} original medias...".format(output_len, initial_len))
        return filtered_media

    def photos_from(self, location):
        """
        :type location: commons.spatial.Location
        :rtype: dict
        """
        url = "https://api.instagram.com/v1/media/search?lat={}&lng={}&access_token={}".format(location.latitude,
                                                                                               location.longitude,
                                                                                               self.access_token)
        self.logger.info("Instagram client calls photos_from with location: {}...".format(location))
        response = requests.get(url)
        return response.json()

# def get_authorization_url():
#     """
#     :return: An URL that should be opened in browser (GET), after redirection there will be authorization_code in URL.
#     :rtype: str
#     """
#     return AUTHORIZE_URL_FORMAT.format(CLIENT_ID, REDIRECT_URI)
#
#
# def get_access_token_command(authorization_code):
#     """
#     :type authorization_code: str
#     :return: Returns a command that needs to be executed in bash to retrieve access token
#     :rtype: str
#     """
#     return "curl -F 'client_id={}' -F 'client_secret={}' -F 'grant_type=authorization_code' -F 'redirect_uri={}' -F 'code={}' {}".format(
#         CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, authorization_code, ACCESS_TOKEN_URL)
