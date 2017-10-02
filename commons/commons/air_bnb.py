from commons.model import Model, Location, Price


def build_air_bnb_listing_object(air_bnb_response_dict):
    """
    :type air_bnb_response_dict: dict[str | dict]
    :rtype: commons.air_bnb.AirBnBListing
    """
    air_bnb_listing = air_bnb_response_dict.get("listing")
    id = int(air_bnb_listing.get("id"))
    city = air_bnb_listing.get("city")
    lat = float(air_bnb_listing.get("lat"))
    lng = float(air_bnb_listing.get("lng"))
    name = air_bnb_listing.get("name")
    person_capacity = int(air_bnb_listing.get("person_capacity"))
    primary_host_name = air_bnb_listing.get("primary_host").get("first_name")
    primary_host_picture_url = air_bnb_listing.get("primary_host").get("picture_url")
    property_type = air_bnb_listing.get("property_type")
    public_address = air_bnb_listing.get("public_address")
    star_rating = air_bnb_listing.get("star_rating")
    bedroom_count = air_bnb_listing.get("bedrooms")
    bed_count = air_bnb_listing.get("beds")
    picture_urls = air_bnb_listing.get("picture_urls")

    air_bnb_pricing = air_bnb_response_dict.get("pricing_quote")
    price_value = float(air_bnb_pricing.get("localized_nightly_price"))
    price_currency = air_bnb_pricing.get("localized_currency")

    return AirBnBListing(id=id, name=name, type=property_type, city=city, public_address=public_address,
                         location=Location(latitude=lat, longitude=lng), star_rating=star_rating,
                         person_capacity=person_capacity, host_person_name=primary_host_name,
                         host_person_picture=primary_host_picture_url, bedroom_count=bedroom_count, bed_count=bed_count,
                         picture_urls=picture_urls, price=Price(value=price_value, currency=price_currency))


class AirBnBListing(Model):
    def __init__(self, id, name, type, city, public_address, location, star_rating, person_capacity, host_person_name,
                 host_person_picture, bedroom_count, bed_count, picture_urls, price):
        """
        :type id: int
        :type name: str
        :type type: str
        :type city: str
        :type public_address: str
        :type location: commons.model.Location
        :type star_rating: float
        :type person_capacity: int
        :type host_person_name: str
        :type host_person_picture: str
        :type bedroom_count: int
        :type bed_count: int
        :type picture_urls: list[str]
        :type price: commons.model.Price
        """
        self.price = price
        self.id = id
        self.name = name
        self.type = type
        self.city = city
        self.public_address = public_address
        self.location = location
        self.star_rating = star_rating
        self.person_capacity = person_capacity
        self.host_person_name = host_person_name
        self.host_person_picture = host_person_picture
        self.room_count = bedroom_count
        self.bed_count = bed_count
        self.picture_urls = picture_urls
