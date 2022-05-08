from django.core.exceptions import ValidationError


def is_phone(val: str):
    """
    Validates a phone number
    """
    if not val.isnumeric() or len(val) != 10:
        raise ValidationError(f'"{val}" is not a valid number')
