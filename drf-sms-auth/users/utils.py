from rest_framework import exceptions


def send_sms(phone, code):
    print(f"{code} for {phone}")


def auth_rule(user):
    if user is not None and user.is_active:
        if user.is_code_expired():
            raise exceptions.AuthenticationFailed("Code has expired")
        return True
