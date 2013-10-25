class BaseManager:

    def __init__(self):
        self.description = None
        self.manufacturer = None
        self.model = None
        self.firmware_version = None
        self.hardware_version = None
        self.parser_type = None
        self.response_manager = None
        self.request_manager = None
        self.comment = None

class BaseResponseManager:
    """
    This is the base class that defines which methods a ResponseManager
    must implement.
    """

    def get_login_credentials(self):
        raise NotImplementedError

    def get_filter_type(self):
        raise NotImplementedError

    def get_filter_list(self):
        raise NotImplementedError

    def get_client_list(self):
        raise NotImplementedError


class BaseRequestManager:
    """
    This is the base class that defines which methods a RequestManager
    must implement.
    """

    def get_login_credentials(self):
        raise NotImplementedError

    def get_filter_type(self):
        raise NotImplementedError

    def get_filter_list(self):
        raise NotImplementedError

    def get_client_list(self):
        raise NotImplementedError
