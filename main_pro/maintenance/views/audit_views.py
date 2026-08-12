# maintenance/views/audit_views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from maintenance.base.permissions import IsAdmin
from maintenance.serializers.audit_serializer import AuditLogSerializer
from maintenance.selectors.auditlog_selectors import get_audit_logs
from maintenance.base.pagination import DefaultPagination


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les journaux d'audit.
    - Accessible uniquement en lecture
    - Réservé aux administrateurs
    - Supporte recherche, tri et pagination
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = DefaultPagination

    search_fields = ["action", "user__username", "model"]
    ordering_fields = ["timestamp", "action", "user__username"]
    ordering = ["-timestamp"]
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self):
        qs = get_audit_logs().select_related("user")

        # 🔍 filtres avancés via query params
        action = self.request.query_params.get("action")
        user = self.request.query_params.get("user")
        model = self.request.query_params.get("model")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if action:
            qs = qs.filter(action=action)
        if user:
            qs = qs.filter(user__username=user)
        if model:
            qs = qs.filter(model=model)
        if start_date:
            qs = qs.filter(timestamp__gte=start_date)
        if end_date:
            qs = qs.filter(timestamp__lte=end_date)

        return qs
