from rest_framework import serializers

from assets.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'phone_number',
            'mobile_number',
            'url'
        )
