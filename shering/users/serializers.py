from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, _):
        code = User.objects.make_random_password(4, "0123456789")
        instance.set_password_and_send_code(instance.phone, code)
        instance.save()
        return instance
