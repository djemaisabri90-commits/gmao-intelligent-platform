from maintenance.base.base_serializer import BaseSerializer
from rest_framework import serializers
from maintenance.models import Rapport

class RapportSerializer(BaseSerializer):
    workorder_id = serializers.IntegerField(source="workorder.id", read_only=True)

    class Meta:
        model = Rapport
        fields = '__all__'