from emserver import settings
import logging
import re
import string
import random

#log = settings.LOGGER

def re_first_match(regex, string):
    """
    Returns the first match of regex in string.
    """
    match = re.search(regex, string)
    if match:
        return match.group()
    return None

def re_first_capture(regex, string):
    """
    Returns the first capture of regex in string. This assumes regex has a
    capture group defined. E.g.

    re_first_capture(r'some(\w+)\s', 'Something sometime someday')

    Returns 'time'
    """
    match = re.search(regex, string)
    if match:
        return match.group(1)
    return None

def random_string(str_len=10):
    """
    Returns a random string of upper-case letters and numbers, up to
    str_len characters in length. Default is 10 characters.
    """
    return ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in range(str_len))
