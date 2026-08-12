from rest_framework import serializers
from maintenance.models import Signalement


class SignalementWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signalement
        fields = [
            "id",
            "machine",
            "description",
            "source",
            "created_at"
        ]

class SignalementReadSerializer(serializers.ModelSerializer):

    machine_nom = serializers.CharField(source="machine.nom", read_only=True)
    cree_par_username = serializers.CharField(source="cree_par.username", read_only=True)

    class Meta:
        model = Signalement
        fields = "__all__"
