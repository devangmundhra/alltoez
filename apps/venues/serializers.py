from rest_framework import serializers

from apps.venues.models import Venue


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = ('name', 'latitude', 'longitude', 'phone_number', 'neighborhood', 'address', 'slug')

    def get_address(self, obj):
        return obj.display_address()

    def get_phone_number(self, obj):
        phone_number = obj.phone_number
        if phone_number:
            phone_number = phone_number.as_national
        return phone_number
