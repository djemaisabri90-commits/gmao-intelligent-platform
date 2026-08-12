# maintenance/views/machine_views.py


from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from maintenance.base.pagination import MachinePagination
from maintenance.base.permissions import IsAdmin, IsExpert, IsTechnicienOrAdmin
from maintenance.models import Machine
from maintenance.serializers.machine_serializer import MachineSerializer
from maintenance.services.machine_service import (
    create_machine,
    update_machine,
    delete_machine,
    can_user_edit_machine
)
from maintenance.selectors.machine_selectors import (
    get_machine_list,
    get_machine_detail,
    get_machine_stats
)
from maintenance.services.audit_service import audit_action


class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = MachinePagination
    def get_queryset(self):
        filters = {}
        etat = self.request.query_params.get('etat')
        if etat:
            filters['etat'] = etat
        return get_machine_list(filters=filters, with_workorders=True)

    def perform_create(self, serializer):
        data = serializer.validated_data
        machine = create_machine(**data)
        audit_action(self.request, "create_machine", machine)
        serializer.instance = machine

    def perform_update(self, serializer):
        machine = self.get_object()
        if not can_user_edit_machine(self.request.user, machine):
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette machine.")
        updated = update_machine(machine, serializer.validated_data)
        audit_action(self.request, "update_machine", updated)
        serializer.instance = updated

    def perform_destroy(self, instance):
        if not can_user_edit_machine(self.request.user, instance):
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette machine.")
        audit_action(self.request, "delete_machine", instance)
        delete_machine(instance)

    @action(detail=False, methods=['get'], url_path='statistiques')
    def statistiques(self, request):
        """
        Retourne des statistiques globales sur les machines :
        - total
        - par état
        - par type
        """
        stats = get_machine_stats()
        return Response(stats)

    @action(detail=True, methods=['get'], url_path='resume')
    def resume_machine(self, request, pk=None):
        """
        Retourne le résumé détaillé d'une machine :
        - état actuel
        - nombre de WorkOrders
        - résumé des WorkOrders par état
        """
        try:
            machine = get_machine_detail(pk, with_workorders=True)
        except Machine.DoesNotExist:
            return Response({"detail": "Machine non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(machine)
        return Response(serializer.data)
    