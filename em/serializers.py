from rest_framework import serializers
from em import models

class RouterSerializer(serializers.ModelSerializer):

    features = serializers.RelatedField(many=True)

    class Meta:
        model = models.Router
        exclude = ('created', 'modified', 'comments')


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device
        exclude = ('first_seen', 'last_seen', 'times_seen')

class MacManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MacManufacturer
        exclude = ('mac_prefix')

class DictionaryField(serializers.WritableField):

    def to_native(self, obj):
        return obj

    def from_native(self, data):
        return data

class RouterRequestSerializer(serializers.Serializer):

    url = serializers.CharField(required=True)
    method = serializers.CharField(required=True)
    port = serializers.IntegerField(required=True)
    headers = DictionaryField(required=False)
    data = DictionaryField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.url = attrs.get('url', instance.url)
            instance.port = attrs.get('port', instance.port)
            instance.method = attrs.get('method', instance.method)
            instance.headers = attrs.get('headers', instance.headers)
            instance.data = attrs.get('data', instance.data)
            return instance
        return models.RouterRequest(**attrs)

class RouterResponseSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    method = serializers.CharField(required=True)
    status_code = serializers.IntegerField(required=True)
    port = serializers.IntegerField(required=True)
    headers = DictionaryField(required=False)
    body = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.url = attrs.get('url', instance.url)
            instance.port = attrs.get('port', instance.port)
            instance.method = attrs.get('method', instance.method)
            instance.status_code = attrs.get(
                'status_code', instance.status_code)
            instance.headers = attrs.get('headers', instance.headers)
            instance.body = attrs.get('body', instance.body)
            return instance
        return models.RouterResponse(**attrs)
