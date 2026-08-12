from rest_framework import serializers
from maintenance.models import PasswordResetRequest

class PasswordResetRequestSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = PasswordResetRequest
        fields = [
            "id",
            "username",
            "status",
            "created_at",
            "processed_at",
        ]