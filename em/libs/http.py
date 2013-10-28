from em.libs.json_serializable import JsonSerializable

class RouterRequest(JsonSerializable):
    """
    This class contains information about HTTP requests that the client will
    have to send to the router.
    """
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.headers = kwargs.get('headers')
        self.data = kwargs.get('data')


class RouterResponse(JsonSerializable):
    """
    This class contains information about an HTTP response that our remote
    client received and then passed back to the server.
    """

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.status_code = kwargs.get('status_code')
        self.headers = kwargs.get('headers')
        self.body = kwargs.get('body')

    def __str__(self):
        return "HttpResponse to {0} {1}".format(self.method, self.url)
