from rest_framework import serializers
from maintenance.models import Log
from maintenance.serializers.utilisateur_serializer import UtilisateurReadSerializer
from maintenance.serializers.workorder_serializers import WorkOrderSerializer
from maintenance.serializers.machine_serializer import MachineSerializer


class LogSerializer(serializers.ModelSerializer):
    user_detail = UtilisateurReadSerializer(source="user", read_only=True)
    workorder_detail = WorkOrderSerializer(source="workorder", read_only=True)
    machine_detail = MachineSerializer(source="machine", read_only=True)

    class Meta:
        model = Log
        fields = [
            "id",
            "workorder",
            "workorder_detail",
            "machine",
            "machine_detail",
            "user",
            "user_detail",
            "action",
            "etat_intervention",
            "metadata",
            "date_action",
        ]
        read_only_fields = ["date_action"]
