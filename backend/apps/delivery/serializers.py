from rest_framework import serializers
from .models import DeliveryPartner, DeliveryStatus

class DeliveryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPartner
        fields = '__all__'
        read_only_fields = ('user', 'average_rating')

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'
