from emserver import settings
import logging
import re

#log = settings.LOGGER

def re_first_match(regex, string):
    match = re.search(regex, string)
    if match:
        return match.group()
    return None

def re_first_capture(regex, string):
    match = re.search(regex, string)
    if match:
        return match.group(1)
    return None
