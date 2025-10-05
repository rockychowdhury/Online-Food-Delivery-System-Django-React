
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import status

from apps.common.utils import APIResponse, ResponseMessages
from apps.common.permissions import IsObjectOwnerOrRolePermission,IsAuthenticatedAndVerified
from .models import Country, UserAddress
from .serializers import CountrySerializer, AddressSerializer, UserAddressSerializer


class CountryListView(APIView):
    """List all countries"""
    permission_classes = [IsAuthenticatedAndVerified]
    
    def get(self, request):
        countries = Country.objects.filter(is_active=True).order_by('country_name')
        serializer = CountrySerializer(countries, many=True)
        
        return APIResponse.success(
            message=ResponseMessages.RETRIEVED_SUCCESS,
            data=serializer.data
        )


class AddressListCreateView(APIView):
    """List user addresses and create new ones"""
    permission_classes = [IsAuthenticatedAndVerified]
    
    def get(self, request):
        """Get user's addresses"""
        user_addresses = UserAddress.objects.filter(
            user=request.user, 
            is_active=True
        ).select_related('address', 'address__country').order_by('-is_default', '-created_at')
        
        serializer = UserAddressSerializer(user_addresses, many=True)
        
        return APIResponse.success(
            message=ResponseMessages.RETRIEVED_SUCCESS,
            data=serializer.data
        )
    
    def post(self, request):
        """Create new address for user"""
        # First create the address
        address_serializer = AddressSerializer(data=request.data)
        if not address_serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=address_serializer.errors,
                error_code="ADDRESS_VALIDATION_ERROR"
            )
        
        address = address_serializer.save()
        
        # Then create user address mapping
        user_address_data = {
            'address_id': address.id,
            'address_type': request.data.get('address_type', 'home'),
            'label': request.data.get('label', ''),
            'is_default': request.data.get('is_default', False),
        }
        
        user_address_serializer = UserAddressSerializer(data=user_address_data)
        if not user_address_serializer.is_valid():
            address.delete()  # Clean up created address
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=user_address_serializer.errors,
                error_code="USER_ADDRESS_VALIDATION_ERROR"
            )
        
        user_address = user_address_serializer.save(user=request.user)
        
        response_serializer = UserAddressSerializer(user_address)
        return APIResponse.success(
            message=ResponseMessages.CREATED_SUCCESS,
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED
        )


class AddressDetailView(APIView):
    """Retrieve, update, delete specific address"""
    permission_classes = [IsAuthenticatedAndVerified, IsObjectOwnerOrRolePermission]
    
    def get_object(self, pk, user):
        """Get user address object"""
        try:
            return UserAddress.objects.select_related('address', 'address__country').get(
                id=pk,
                user=user,
                is_active=True
            )
        except UserAddress.DoesNotExist:
            raise NotFound("Address not found")
    
    def get(self, request, pk):
        """Get specific address"""
        user_address = self.get_object(pk, request.user)
        serializer = UserAddressSerializer(user_address)
        
        return APIResponse.success(
            message=ResponseMessages.RETRIEVED_SUCCESS,
            data=serializer.data
        )
    

    #TODO: review and understand the code
    def patch(self, request, pk):
        """Update specific address"""
        user_address = self.get_object(pk, request.user)
        
        # Update UserAddress fields
        user_address_serializer = UserAddressSerializer(
            user_address,
            data=request.data,
            partial=True
        )
        
        if not user_address_serializer.is_valid():
            return APIResponse.error(
                message=ResponseMessages.VALIDATION_ERROR,
                errors=user_address_serializer.errors,
                error_code="VALIDATION_ERROR"
            )
        
        # Update Address fields if provided
        address_data = {k: v for k, v in request.data.items() if k in ['street_address', 'apartment_number', 'city', 'state', 'postal_code', 'country', 'latitude', 'longitude', 'delivery_instructions']}
        
        if address_data:
            address_serializer = AddressSerializer(
                user_address.address,
                data=address_data,
                partial=True
            )
            if not address_serializer.is_valid():
                return APIResponse.error(
                    message=ResponseMessages.VALIDATION_ERROR,
                    errors=address_serializer.errors,
                    error_code="ADDRESS_VALIDATION_ERROR"
                )
            address_serializer.save()
        
        user_address = user_address_serializer.save()
        response_serializer = UserAddressSerializer(user_address)
        
        return APIResponse.success(
            message=ResponseMessages.UPDATED_SUCCESS,
            data=response_serializer.data
        )
    
    def delete(self, request, pk):
        """Soft delete address"""
        user_address = self.get_object(pk, request.user)
        user_address.soft_delete()
        
        return APIResponse.success(message=ResponseMessages.DELETED_SUCCESS)