from commons.model import Model, Location


def build_instagram_media_object(media_dict):
    """
    :type media_dict: dict
    :rtype: commons.instagram.InstagramMedia
    """
    location = None
    if media_dict.get("location"):
        location = InstagramLocation(latitude=media_dict.get("location").get("latitude"),
                                     longitude=media_dict.get("location").get("longitude"),
                                     location_id=media_dict.get("location").get("id"),
                                     location_name=media_dict.get("location").get("name"))
    return InstagramMedia(media_id=media_dict.get("id"),
                          location=location,
                          media_type=media_dict.get("type"),
                          img_url_320=media_dict.get("images").get("low_resolution").get("url"),
                          img_url_640=media_dict.get("images").get("standard_resolution").get("url"),
                          created_timestamp=int(media_dict.get("created_time")),
                          likes_count=media_dict.get("likes").get("count"),
                          tags=media_dict.get("tags"))


class InstagramLocation(Location):
    def __init__(self, latitude, longitude, location_id, location_name):
        """
        :type latitude: float
        :type longitude: float
        :type location_id: int
        :type location_name: basestring
        """
        super(InstagramLocation, self).__init__(latitude, longitude)
        self.location_id = location_id
        self.location_name = location_name

    def to_meta(self):
        """
        :rtype: commons.model.Location
        """
        return Location(self.latitude, self.longitude)


class InstagramMedia(Model):
    def __init__(self, media_id, location, media_type, img_url_320, img_url_640, created_timestamp, likes_count, tags):
        """
        :type media_id: str
        :type location: commons.instagram.InstagramLocation | None
        :type media_type: str
        :type img_url_320: str
        :type img_url_640: str
        :type created_timestamp: int
        :type likes_count: int
        :type tags: list[str]
        """
        self.tags = tags
        self.likes_count = likes_count
        self.created_timestamp = created_timestamp
        self.img_url_640 = img_url_640
        self.img_url_320 = img_url_320
        self.media_type = media_type
        self.location = location
        self.media_id = media_id

    def is_image(self):
        return self.media_type == "image"

    @classmethod
    def from_serializable(cls, serializable):
        """
        :type serializable: dict
        :rtype: commons.instagram.InstagramMedia
        """
        likes_count = serializable.get("likes_count")
        created_timestamp = int(serializable.get("created_timestamp"))
        img_url_640 = serializable.get("img_url_640")
        img_url_320 = serializable.get("img_url_320")
        media_type = serializable.get("media_type")
        if serializable.get("location"):
            location = InstagramLocation.from_serializable(serializable.get("location"))
        else:
            location = None
        media_id = serializable.get("media_id")
        tags = serializable.get("tags")
        return InstagramMedia(media_id, location, media_type, img_url_320, img_url_640,
                              created_timestamp, likes_count, tags)

    def to_serializable(self):
        """
        :rtype: dict
        """
        output_dict = super(InstagramMedia, self).to_serializable()
        if self.location:
            output_dict.update({"location": self.location.to_serializable()})
        return output_dict
