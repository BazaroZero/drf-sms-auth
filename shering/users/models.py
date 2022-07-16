from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager
from .utils import send_sms


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, max_length=20)
    code_created_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "phone"
    objects = UserManager()

    def set_password_and_send_code(self, phone: str, raw_password: str) -> None:
        super().set_password(raw_password)
        send_sms(phone, raw_password)
