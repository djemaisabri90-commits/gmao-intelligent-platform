# maintenance/views/log_views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models  # ✅ Import nécessaire

from maintenance.models import Log
from maintenance.serializers.log_serializer import LogSerializer


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les journaux (logs).
    - Accessible uniquement en lecture
    - Filtrage par machine, workorder, utilisateur
    """
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Log.objects.select_related("workorder", "machine", "user").order_by("-date_action")

        # Filtrage par query params
        machine_id = self.request.query_params.get("machine_id")
        workorder_id = self.request.query_params.get("workorder_id")
        user_id = self.request.query_params.get("user_id")

        if machine_id:
            qs = qs.filter(machine_id=machine_id)
        if workorder_id:
            qs = qs.filter(workorder_id=workorder_id)
        if user_id:
            qs = qs.filter(user_id=user_id)

        return qs

    @action(detail=False, methods=["get"], url_path="resume")
    def resume_logs(self, request):
        """
        Retourne un résumé global des logs :
        - total
        - par action
        - par utilisateur
        """
        qs = self.get_queryset()

        stats = {
            "total": qs.count(),
            "by_action": dict(qs.values("action").annotate(count=models.Count("id")).values_list("action", "count")),
            "by_user": dict(qs.values("user__username").annotate(count=models.Count("id")).values_list("user__username", "count")),
        }
        return Response(stats, status=status.HTTP_200_OK)
