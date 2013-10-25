from em.libs include NetClient, Router

class NetState:

    def __init__(self, *args, **kwargs):
        self.clients = kwargs.get('clients')
        self.manager = kwargs.get('manager')
        self.router = kwargs.get('router')
