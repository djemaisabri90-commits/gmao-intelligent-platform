from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from maintenance.base.permissions import IsAdminOrExpert

from maintenance.serializers.rapport_serializer import RapportSerializer
from maintenance.selectors.rapport_selectors import get_rapports
from maintenance.services.rapport_service import create_rapport


class RapportViewSet(viewsets.ModelViewSet):

    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated, IsAdminOrExpert]

    def get_queryset(self):
        return get_rapports()

    def perform_create(self, serializer):
        create_rapport(serializer.validated_data)