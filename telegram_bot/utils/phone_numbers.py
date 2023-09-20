from typing import Optional

import phonenumbers


def validate_phone_number(
    raw_phone: str, raise_exception: bool = False, phone_number=None
) -> Optional[phonenumbers.phonenumber.PhoneNumber]:
    try:
        phone_number = phonenumbers.parse(raw_phone, "RU")
    except phonenumbers.phonenumberutil.NumberParseException as E:
        if raise_exception:
            raise E
    if phone_number:
        if phonenumbers.is_valid_number(phone_number):
            return phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
