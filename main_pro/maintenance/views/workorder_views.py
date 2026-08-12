# maintenance/views/workorder_views.py

from django.db import models

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from maintenance.base.pagination import WorkOrderPagination
from maintenance.models import WorkOrder, Machine, Intervention
from maintenance.serializers import WorkOrderSerializer
from maintenance.base.permissions import IsAdminOrExpert
from maintenance.services.workorder_services import (
    create_workorder,
    update_workorder,
    delete_workorder,
    can_user_edit_workorder,
)
from maintenance.services.audit_service import audit_action
from maintenance.selectors.workorder_selectors import (
    get_workorder_list,
    get_workorder_stats,
    get_workorder_summary_for_machine,
)


class WorkOrderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WorkOrderPagination  # ✅ ajout pagination


    # =====================================================
    # 📋 QUERYSET
    # =====================================================
    def get_queryset(self):
        user = self.request.user
        filters = {}
        if priorite_param := self.request.query_params.get('priorite'):
            filters['priorite'] = priorite_param
        if type_param := self.request.query_params.get('type'):
            filters['type'] = type_param
        if machine_param := self.request.query_params.get('machine'):
            filters['machine_id'] = machine_param

        qs = get_workorder_list(filters=filters, with_relations=True)
        role = getattr(user, "role", None)

        if role in ["admin", "expert"]:
            return qs

        if role == "technicien":
            # ✅ inclure les deux relations
            return qs.filter(
                models.Q(techniciens=user) |
                models.Q(interventions__techniciens=user)
            ).distinct()

        if role == "operateur":
            # opérateur voit uniquement ses propres signalements
            return qs.filter(signalement__cree_par=user)

        return qs.none()


        #return get_workorder_list(filters=filters, user=self.request.user)

    # =====================================================
    # ➕ CREATE
    # =====================================================
    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data.pop('cree_par', None)  # sécurité
        workorder = create_workorder(**data, cree_par=user)
        audit_action(self.request, "create", workorder)
        serializer.instance = workorder

    # =====================================================
    # ✏️ UPDATE
    # =====================================================
    def perform_update(self, serializer):
        workorder = self.get_object()
        if not can_user_edit_workorder(self.request.user, workorder):
            raise PermissionDenied("Modification non autorisée.")
        updated = update_workorder(workorder, serializer.validated_data)
        audit_action(self.request, "update", updated)
        serializer.instance = updated

    # =====================================================
    # ❌ DELETE
    # =====================================================
    def perform_destroy(self, instance):
        if not can_user_edit_workorder(self.request.user, instance):
            raise PermissionDenied("Suppression non autorisée.")
        audit_action(self.request, "delete", instance)
        delete_workorder(instance)

    # =====================================================
    # 📊 STATISTIQUES
    # =====================================================
    @action(detail=False, methods=['get'], url_path='statistiques')
    def statistiques(self, request):
        stats = get_workorder_stats(user=request.user)
        return Response(stats)

    # =====================================================
    # 🏭 RESUME MACHINE
    # =====================================================
    @action(detail=False, methods=['get'], url_path='resume-machine/(?P<machine_id>[^/.]+)')
    def resume_machine(self, request, machine_id=None):
        try:
            machine = Machine.objects.get(id=machine_id)
        except Machine.DoesNotExist:
            return Response({"detail": "Machine non trouvée."},
                            status=status.HTTP_404_NOT_FOUND)

        summary = get_workorder_summary_for_machine(machine_id)
        summary['machine'] = {'id': machine.id, 'nom': machine.nom}
        return Response(summary)


# =====================================================
# 🔄 AUTO-CLOTURE VIA INTERVENTIONS
# =====================================================
@receiver(post_save, sender=Intervention)
def auto_close_workorder(sender, instance, **kwargs):
    workorder = instance.workorder
    if workorder:
        # Vérifier si toutes les interventions sont validées
        all_validated = all(i.date_validation for i in workorder.interventions.all())
        if all_validated and not workorder.date_cloture:
            workorder.date_cloture = timezone.now()
            workorder.save()
