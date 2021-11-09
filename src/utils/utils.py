"""
This module provides the micro web server implementing the pokedex.
"""

HTML_ESCAPE_SEQUENCES = ['\f', '\r', '\n', '\t']


def replace_escape(msg: str, substr: str = ' ') -> str:
    """
    Replaces the HTML escape sequences in the given message with the given substr.

    :param msg: the message
    :param substr: the replacing substr
    :return: the message with no HTML escape sequences
    """
    replaced = msg
    for e in HTML_ESCAPE_SEQUENCES:
        replaced = replaced.replace(e, substr)
    return replaced
