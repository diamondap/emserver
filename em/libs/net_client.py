
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

    def merge(self, other):
        """
        Merges all of the values from another NetClient object into this
        NetClient object. Anytime the other object's attribute value is
        not None, it will overwrite this NetClient's attribute value.

        Returns self.
        """
        if self.mac != other.mac:
            raise ValueError('Cannot merge NetClient objects with '
                             'different MAC addresses.')
        for key in self.__dict__:
            val = getattr(self, key)
            other_val = getattr(other, key)
            if other_val is not None and other_val != '':
                setattr(self, key, other_val)
        return self


    @classmethod
    def merge_lists(self, list1, list2):
        """
        Merges two lists of NetClient objects. The resulting lists will
        contain all the members of both lists, with no duplicates. The
        merge uses the following logic:

        1. If an object's property is None in one list and not None in the
        other list, the non-None property wins.
        2. If a property is not None in both lists, the value of the property
        in list2 wins.

        NetClient objects are considered unique by MAC address.

        You may run into problems if either list includes the same MAC address
        more than once.
        """
        macs = set()
        clients = []
        for client in list1:
            list2_client = next((c for c in list2 if c.mac == client.mac), None)
            if list2_client is not None:
                client = client.merge(list2_client)
            if not client.mac in macs:
                clients.append(client)
                macs.add(client.mac)
            else:
                raise ValueError("Mutilple entries in list1 have MAC "
                                 "address {0}".format(client.mac))
        for client in list2:
            seen = set()
            if client.mac in seen:
                raise ValueError("Mutilple entries in list2 have MAC "
                                 "address {0}".format(client.mac))
            if not client.mac in macs:
                clients.append(client)
                macs.add(client.mac)
            seen.add(client.mac)
        return clients
