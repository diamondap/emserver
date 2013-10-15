import re

# Manager for MediaLink MWN_WAPR300N Router

class Manager:

    def __init__(self):
        self.manufacturer = 'MediaLink'
        self.model = 'MWN-WAPR300N'
        self.parser_type = 'regex'
        self.parser_comment = ("This router's HTML is unparsable because "
                               "it uses document.write everywhere.")
