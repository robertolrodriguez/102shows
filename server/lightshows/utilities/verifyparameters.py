"""
Verify Parameters
(c) 2016 Simon Leiner

functions that validate input parameters and exceptions with error messages
if the input does not fit the requirements. These are at the moment:

 - numeric
 - not_negative_numeric
 - positive_numeric

 - integer
 - not_negative_integer
 - positive_integer

 - boolean

 - rgb_color_tuple

The module defines some own exception classes:
 - InvalidParameters (as used by the functions above)
 - InvalidConf
 - InvalidStrip
"""


def numeric(candidate, param_name: str = None, minimum: float = None, maximum: float = None):
    """
    number (between minimum and maximum)

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    :param minimum: minimum (of a closed set)
    :param maximum: maximum (of a closed set)
    """
    if param_name:
        debug_str = "Parameter \"{name}\" must be a number".format(name=param_name)
    else:
        debug_str = "Parameter must be a number"

    if minimum is not None and maximum is not None:
        debug_str += " between {min} and {max}".format(min=minimum, max=maximum)
    elif minimum is not None:
        debug_str += " >= {}".format(minimum)
    elif maximum is not None:
        debug_str += " <= {}".format(maximum)

    debug_str += "! (got: {})".format(candidate)

    if type(candidate) not in (float, int):
        raise InvalidParameters(debug_str)
    if minimum is not None and candidate < minimum:
        raise InvalidParameters(debug_str)
    if maximum is not None and candidate > maximum:
        raise InvalidParameters(debug_str)


def not_negative_numeric(candidate, param_name: str = None):
    """
    a not-negative number => 0 or above

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if type(candidate) not in (float, int) or candidate < 0:
        if param_name:
            debug_str = "Parameter \"{name}\" must be a non-negative number!".format(name=param_name)
        else:
            debug_str = "Parameter must be a not-negative number!"
        raise InvalidParameters(debug_str)


def positive_numeric(candidate, param_name: str = None):
    """
    a positive number => greater than 0

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if type(candidate) not in (float, int) or candidate <= 0:
        if param_name:
            debug_str = "Parameter \"{name}\" must be a positive number!".format(name=param_name)
        else:
            debug_str = "Parameter must be a positive number!"
        raise InvalidParameters(debug_str)


def integer(candidate, param_name: str = None, minimum: float = None, maximum: float = None):
    """
    integer (between minimum and maximum)

    :param param_name: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    :param minimum: minimum
    :param maximum: maximum
    """
    if param_name:
        debug_str = "Parameter \"{name}\" must be an integer".format(name=param_name)
    else:
        debug_str = "Parameter must be an integer"

    if minimum is not None and maximum is not None:
        debug_str += " between {min} and {max}".format(min=minimum, max=maximum)
    elif minimum is not None:
        debug_str += " >= {}".format(minimum)
    elif maximum is not None:
        debug_str += " <= {}".format(maximum)

    debug_str += "! (got: {})".format(candidate)

    if type(candidate) is not int:
        raise InvalidParameters(debug_str)
    if minimum is not None and candidate < minimum:
        raise InvalidParameters(debug_str)
    if maximum is not None and candidate > maximum:
        raise InvalidParameters(debug_str)


def not_negative_integer(candidate, param_name: str = None):
    """
    a not-negative integer => 0,1,2,3,...

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if type(candidate) is not int or candidate < 0:
        if param_name:
            debug_str = "Parameter \"{name}\" must be a non-negative integer!".format(name=param_name)
        else:
            debug_str = "Parameter must be a not-negative integer!"
        raise InvalidParameters(debug_str)


def positive_integer(candidate, param_name: str = None):
    """
    a positive integer => greater than 0 => 1 or above

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if type(candidate) is not int or candidate <= 0:
        if param_name:
            debug_str = "Parameter \"{name}\" must be a positive integer!".format(name=param_name)
        else:
            debug_str = "Parameter must be a positive integer!"
        raise InvalidParameters(debug_str)


def boolean(candidate, param_name: str = None):
    """
    a boolean value: True or False

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if type(candidate) is not bool:
        if param_name:
            debug_str = "Parameter \"{name}\" must be a boolean value!".format(name=param_name)
        else:
            debug_str = "Parameter must be a boolean value!"
        raise InvalidParameters(debug_str)


def rgb_color_tuple(candidate, param_name: str = None):
    """
    An RGB color tuple. It must contain three integer components between 0 and 255.

    :param candidate: the object to be tested
    :param param_name: name of the parameter (to be included in the error message)
    """
    if param_name:
        debug_str = "Parameter \"{name}\" must be an RGB color tuple!".format(name=param_name)
    else:
        debug_str = "Parameter must be an RGB color tuple!"

    if type(candidate) is not tuple:
        raise InvalidParameters(debug_str)

    if len(candidate) is not 3:  # an rgb tuple has three components
        raise InvalidParameters(debug_str)

    for component in candidate:
        if type(component) is not int:
            raise InvalidParameters(debug_str)
        if not (0 <= component <= 255):
            raise InvalidParameters(debug_str)


class InvalidStrip(Exception):
    """
    use if something is wrong with the strip
    for example: not enough LEDs to run the selected lightshow
    """
    pass


class InvalidConf(Exception):
    """
    use if something in the configuration will not work
    for what the user has chosen
    """
    pass


class InvalidParameters(Exception):
    """
    use when given parameters are not valid
    """
    @staticmethod
    def unknown(param_name: str = None):
        if param_name:
            debug_str = "Parameter \"{name}\" is unknown!".format(name=param_name)
        else:
            debug_str = "Parameter is unknown!"
        return InvalidParameters(debug_str)

    @staticmethod
    def missing(param_name: str = None):
        if param_name:
            debug_str = "Parameter \"{name}\" is missing!".format(name=param_name)
        else:
            debug_str = "Parameter is missing!"
        return InvalidParameters(debug_str)
