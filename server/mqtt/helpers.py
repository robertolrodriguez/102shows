"""
Helpers for MQTT
(c) 2016 Simon Leiner

A couple of helper functions (big surprise!) for MQTTControl
"""

import json
import logging as log


class TopicAspect:
    """ information you can get out of an MQTT topic (and on which path hierarchy they are) """
    prefix = 0
    sys_name = 1
    show_name = 3
    command = 4


def get_from_topic(hierarchy_level: int, topic: str) -> str:
    """
    get the string on a specified hierarchy level

    :param hierarchy_level: integer level
    :param topic: string to be analyzed
    :return: part-string of the wanted level
    """
    hierarchy = topic.split(sep="/")
    return hierarchy[hierarchy_level]


def binary_to_string(payload) -> str:
    """
    turn a binary represented string into a python string

    :param payload: binary string
    :return: python string
    """
    string = str(payload)
    stripped_string = string[2:-1]  # remove first two and last character
    return stripped_string


def parse_json_safely(payload: str) -> dict:
    """
    parse a string as JSON object
    logs failures as warnings

    :param payload: string to be parsed
    :return: parsed JSON object (as dict)
    """
    if payload:  # not empty
        try:
            unpacked = json.loads(payload)
        except Exception as error:
            log.warning("Could not parse this payload: {}".format(error))
            return {}
        else:
            if type(unpacked) is not dict:
                log.warning("This payload is not a JSON object!")
                return {}
        return unpacked
    else:
        log.debug("Payload is empty!")
        return {}
