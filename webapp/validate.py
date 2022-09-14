from django.core.exceptions import ValidationError


def validate_title(value):
    if len(value) > 7:
        raise ValidationError("Название должно быть  короче 7 символов")
    return value
