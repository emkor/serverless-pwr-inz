import os


def get_env_variable(variable_name, default=None):
    """
    :type variable_name: str
    :type default: object
    :rtype: str
    """
    return str(os.getenv(variable_name, default))
