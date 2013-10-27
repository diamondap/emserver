import json

# Everything in here is tested in em/tests/unit/libs/http_test.py
# since those classes actually implement these methods.
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
    """
    Converts a list of JsonSerializable objects to JSON.
    """
    return json.dumps(to_list(items))

def list_from_json(json_string, klass):
    """
    Converts a JSON string to a list of items of class klass.
    This assumes you're working with very simple objects of
    type JsonSerializable.
    """
    object_list = []
    dictionaries = json.loads(json_string)
    for dictionary in dictionaries:
        object_list.append(klass(**dictionary))
    return object_list

def to_list(items):
    """
    Converts a list of JsonSerializable objects to a list of dictionaries.
    """
    dictionaries = []
    for item in items:
        if not isinstance(item, JsonSerializable):
            raise ValueError('Items must of type JsonSerializable')
        dictionaries.append(item.__dict__)
    return dictionaries
