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
