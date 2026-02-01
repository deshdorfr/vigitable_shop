from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField()
