from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone):
        user = self.model(phone=phone)
        code = self.make_random_password(4, "0123456789")
        user.set_password_and_send_code(phone, code)
        user.save()
        return user

    def create_superuser(self, phone, password):
        user = self.model(phone=phone)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
