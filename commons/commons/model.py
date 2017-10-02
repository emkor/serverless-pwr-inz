from copy import copy


class Model(object):
    def __str__(self):
        """
        :rtype: str
        """
        return "<{} object: {}>".format(self.__class__.__name__, self.__dict__)

    def __repr__(self):
        """
        :rtype: str
        """
        return self.__str__()

    def __eq__(self, other):
        """
        :type other: commons.model.Model
        :rtype: bool
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        :type other: commons.model.Model
        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        :rtype: str
        """
        return hash(self.__dict__)

    def to_serializable(self):
        return copy(self.__dict__)

    @classmethod
    def from_serializable(cls, serializable):
        """
        :type serializable: dict
        :rtype: object
        """
        return cls(**serializable)


class Location(Model):
    def __init__(self, latitude, longitude):
        """
        :param latitude:  [-90, +90], S/N
        :type latitude: float
        :param longitude: [-180, +180], E/W
        :type longitude: float
        """
        self.latitude = latitude
        self.longitude = longitude
        self._raise_if_not_valid()

    def _raise_if_not_valid(self):
        if not (-90. <= self.latitude <= 90.) or not (-180. <= self.longitude <= 180.):
            raise ValueError("Location is incorrect: {}".format(self.__dict__))


class City(Model):
    def __init__(self, city_name, population, location, country, city_code):
        """
        :type city_name: str
        :type population: int
        :type location: commons.model.Location
        :type country: str
        :param city_code: City code needed for SkyScanner flight retrieval
        :type city_code: str
        """
        self.city_name = city_name
        self.population = population
        self.location = location
        self.country = country
        self.city_code = city_code

    @classmethod
    def from_serializable(cls, serializable):
        """
        :type serializable: dict
        :rtype: commons.model.City
        """
        location = Location.from_serializable(serializable.pop("location"))
        return City(location=location, **serializable)

    def to_serializable(self):
        """
        :rtype: dict
        """
        location_dict = self.location.to_serializable()
        output = super(City, self).to_serializable()
        output.update({"location": location_dict})
        return output


class Price(Model):
    def __init__(self, value, currency):
        """
        :type value: float
        :type currency: str
        """
        self.currency = currency
        self.value = value

    def __repr__(self):
        return "<Price: {} {}>".format(self.value, self.currency)
