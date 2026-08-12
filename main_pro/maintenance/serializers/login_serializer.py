#maintenance/serializers/login_serializer.py

from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
            
        if not user:
            raise serializers.ValidationError("Identifiants invalides")

        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé")

        data["user"] = user
        return data