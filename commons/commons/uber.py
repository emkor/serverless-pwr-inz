from commons.model import Model, Price


def build_uber_product_object(uber_product):
    """
    :type uber_product: dict
    :rtype: commons.uber.UberProduct
    """
    product_id = uber_product.get("product_id")
    product_name = uber_product.get("display_name")
    product_description = uber_product.get("description")
    capacity = uber_product.get("capacity")
    return UberProduct(id=product_id, name=product_name, description=product_description, capacity=capacity)


def build_uber_pricing_object(uber_pricing_dict):
    """
    :type uber_pricing_dict: dict
    :rtype: commons.uber.UberPricing
    """
    product_id = uber_pricing_dict.get("product_id")
    product_name = uber_pricing_dict.get("display_name")
    duration = uber_pricing_dict.get("duration")
    distance = uber_pricing_dict.get("distance")
    currency = uber_pricing_dict.get("currency_code")
    low_estimate = uber_pricing_dict.get("low_estimate")
    high_estimate = uber_pricing_dict.get("high_estimate")
    return UberPricing(product_id=product_id, product_name=product_name,
                       duration=duration, distance=distance,
                       low_estimate=Price(value=low_estimate, currency=currency),
                       high_estimate=Price(value=high_estimate, currency=currency))


class UberPricing(Model):
    def __init__(self, product_id, product_name, duration, distance, low_estimate, high_estimate):
        """
        :type product_id: str
        :type product_name: str
        :type duration: float
        :type distance: float
        :type low_estimate: commons.model.Price
        :type high_estimate: commons.model.Price
        """
        self.product_id = product_id
        self.product_name = product_name
        self.duration = duration
        self.distance = distance
        self.low_estimate = low_estimate
        self.high_estimate = high_estimate

    @classmethod
    def from_serializable(cls, serializable):
        """
        :type serializable: dict
        :rtype: commons.uber.UberPricing
        """
        low_estimate = Price.from_serializable(serializable.pop("low_estimate"))
        high_estimate = Price.from_serializable(serializable.pop("high_estimate"))
        duration = float(serializable.get("duration"))
        distance = float(serializable.get("distance"))
        return UberPricing(serializable.get("product_id"), serializable.get("product_name"), duration,
                           distance, low_estimate, high_estimate)

    def to_serializable(self):
        """
        :rtype: dict
        """
        output_dict = super(UberPricing, self).to_serializable()
        low_estimate_dict = self.low_estimate.to_serializable()
        output_dict.update({"low_estimate": low_estimate_dict})
        high_estimate_dict = self.high_estimate.to_serializable()
        output_dict.update({"high_estimate": high_estimate_dict})
        return output_dict


class UberProduct(Model):
    def __init__(self, id, name, description, capacity):
        """
        :type id: str
        :type name: str
        :type description: str
        :type capacity: int
        """
        self.capacity = capacity
        self.description = description
        self.name = name
        self.id = id
