from rest_framework import serializers
from .models import User, Address


class SignInSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "mobile", "name", "email", "addresses"]
        read_only_fields = ["id", "mobile", "addresses"]
