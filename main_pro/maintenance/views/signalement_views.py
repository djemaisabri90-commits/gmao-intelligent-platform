from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from maintenance.models import Signalement
from maintenance.serializers.signalement_serializer import (
    SignalementWriteSerializer,
    SignalementReadSerializer
)
from maintenance.services.audit_service import audit_action
from maintenance.services.signalement_service import (
    create_signalement,
    close_signalement
)
from maintenance.base.permissions import SignalementPermission, IsTechnicien, IsAdmin


class SignalementViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    """
    def get_permissions(self):

        if self.action == "create":
            return [IsTechnicien()]

        if self.action == "destroy":
            return [IsAdmin()]

        return super().get_permissions()
    """
    #lister signalement
    def get_queryset(self):
        return Signalement.objects.select_related("machine", "cree_par")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SignalementReadSerializer
        return SignalementWriteSerializer
    

    def perform_create(self, serializer):
        instance = create_signalement(
            user=self.request.user,
            **serializer.validated_data
        )
        audit_action(self.request, "create_signal", instance)
        serializer.instance = instance

    


    # action métier
    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        signalement = self.get_object()

        signalement = close_signalement(signalement)
        
        audit_action(self.request, "traite_signal", signalement)


        return Response({"status": "signalement traité"})