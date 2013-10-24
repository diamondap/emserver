
class NetClient:
    """
    Contains information about a single client on the network.
    """
    def __init__(self, *args, **kwargs):
        self.ip = kwargs.get('ip')
        self.mac = kwargs.get('mac')
        self.hostname = kwargs.get('hostname')
        self.conn_type = kwargs.get('conn_type')
        self.device_type = kwargs.get('device_type')
        self.os_type = kwargs.get('os_type')
        self.is_whitelisted = kwargs.get('is_whitelisted')
        self.is_blacklisted = kwargs.get('is_blacklisted')
        self.nickname = kwargs.get('nickname')
