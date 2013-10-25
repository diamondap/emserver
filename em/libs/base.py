class BaseManager:
    pass

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
