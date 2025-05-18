from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
def validate_image_url(value):
    if value and not value.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        raise ValidationError("URL must point to a valid image (PNG, JPG, WEBP, GIF)")