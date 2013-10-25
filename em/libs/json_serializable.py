import json

class JsonSerializable:
    """
    This base class provides methods to serialize relatively
    simple objects to and from JSON. Note that it does not
    handle nested objects, datetimes, or other complex objects.
    It's only for really simple cases!
    """

    @classmethod
    def from_json(self, json_string):
        data = json.loads(json_string)
        return self(**data)

    def to_json(self):
        return json.dumps(self.__dict__)


def list_to_json(items):
    dictionaries = []
    for item in self.items:
        if not isinstance(item, JsonSerializable):
            raise ValueError('Items must of type JsonSerializable')
        dictionaries.append(item.__dict__)
    return json.dumps(dictionaries)

def list_from_json(json_string, klass):
    object_list = []
    dictionaries = json.loads(json_string)
    for dictionary in dictionaries:
        object_list.append(klass(**dictionary))
    return object_list
