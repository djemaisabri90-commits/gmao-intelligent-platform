from rest_framework import serializers
from maintenance.models import Machine
from maintenance.serializers.workorder_serializers import WorkOrderSerializer


class MachineSerializer(serializers.ModelSerializer):
    # Liste des WorkOrders liés
    workorders = WorkOrderSerializer(
        source='workorder_set',
        many=True,
        read_only=True
    )

    # Nombre de WorkOrders liés
    workorder_count = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = [
            'id', 'nom', 'description', 'localisation', 'type',
            'date_installation', 'etat',
            'workorders', 'workorder_count', 'latitude', 'longitude',
        ]

    def get_workorder_count(self, obj):
        return obj.workorder_set.count()
    
    def get_workorder_summary(self, obj):
        summary = {"en_attente": 0, "en_cours": 0, "valide": 0, "clos": 0}
        for wo in obj.workorder_set.all():
            summary[wo.etat] = summary.get(wo.etat, 0) + 1
        return summary
