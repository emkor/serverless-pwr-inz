import datetime
import json
from decimal import Decimal


class DeserializationError(Exception):
    def __init__(self, root_cause, input_json, target_class):
        """
        :type root_cause: Exception
        :type input_json: dict
        :type target_class: class
        """
        self.target_class = target_class
        self.input_json = input_json
        self.root_cause = root_cause

    def __str__(self):
        return "DeserializationError: could not create model {} from: {}. Root cause: {}".format(self.target_class,
                                                                                                 self.input_json,
                                                                                                 self.root_cause)

    def __repr__(self):
        return self.__str__()


def to_json(v):
    """
    :type v: object
    :rtype: str
    """
    return json.dumps(v, default=custom_handling)


def from_json(input_json, target_class):
    """
    :type input_json: str
    :type target_class: class
    :rtype: str
    """
    try:
        input_dict = json.loads(input_json)
        return target_class(**input_dict)
    except Exception as e:
        raise DeserializationError(e, input_json=input_json, target_class=target_class)


def to_json_file(v, file_object):
    """
    :type v: object
    :type file_object: file
    :rtype: str
    """
    return json.dump(v, file_object, default=custom_handling)


def custom_handling(v):
    """
    :type v: object
    :rtype: basestring | int | float | list | dict | None
    """
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    elif isinstance(v, Decimal):
        return float(v)
    elif isinstance(v, set):
        return list(v)
    else:
        return v.__dict__
