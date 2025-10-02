#TODO: review and understand the working with serializers


from rest_framework import serializers
from .models import Country, Address, UserAddress

class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""
    
    class Meta:
        model = Country
        fields = ['id', 'country_code', 'country_name']
        read_only_fields = ['id']

class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    full_address = serializers.CharField(read_only=True)
    
    class Meta:
        model = Address
        fields = [
            'id', 'street_address', 'apartment_number', 'city', 
            'state', 'postal_code', 'country', 'country_name',
            'latitude', 'longitude', 'delivery_instructions',
            'full_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'full_address', 'created_at', 'updated_at']



class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer for UserAddress model"""
    address = AddressSerializer(read_only=True)
    address_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = UserAddress
        fields = [
            'id', 'address', 'address_id', 'address_type', 
            'label', 'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_address_id(self, value):
        """Validate that address exists"""
        try:
            Address.objects.get(id=value, is_active=True)
            return value
        except Address.DoesNotExist:
            raise serializers.ValidationError("Address not found")
