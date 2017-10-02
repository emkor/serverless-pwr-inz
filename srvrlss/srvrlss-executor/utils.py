import json


def read_payload(event):
    """
    :type event: dict[str, str]
    :rtype: dict
    """
    return json.loads(event.get("body") or "")


def build_response(payload, status_code=200):
    """
    :type payload: object | list[object]
    :type status_code: int
    :rtype: dict[str, int | object]
    """
    return {
        "statusCode": status_code,
        "body": json.dumps(payload)
    }
