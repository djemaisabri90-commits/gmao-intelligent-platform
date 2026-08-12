from rest_framework import serializers
from maintenance.models import AuditLog
from maintenance.serializers.utilisateur_serializer import UtilisateurReadSerializer


class AuditLogSerializer(serializers.ModelSerializer):
    user_detail = UtilisateurReadSerializer(source="user", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "user_detail",
            "action",
            "action_display",
            "model",
            "object_id",
            "timestamp",
            "ip_address",
            "user_agent",
            "endpoint",
            "method",
            "changements",
        ]
        read_only_fields = ["timestamp"]
