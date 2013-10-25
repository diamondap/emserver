from em.libs.json_serializable import JsonSerializable

class HttpRequest(JsonSerializable):
    """
    This class contains information about HTTP requests that the client will
    have to send to the router.
    """
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.headers = kwargs.get('headers')
        self.data = kwargs.get('data')
