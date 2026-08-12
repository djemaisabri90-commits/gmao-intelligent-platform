"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from maintenance.services.dashboard_service import build_dashboard_data

@api_view(["GET"])
def dashboard_api(request):

    data = build_dashboard_data()

    return Response(data)
"""

from rest_framework import viewsets

from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response

from maintenance.models import (
    Signalement,
    WorkOrder,
    Intervention,
    PieceUtilisee,
)


def get_dashboard_stats():

    total_pieces = (
        PieceUtilisee.objects.aggregate(
            total=Sum("quantite")
        )["total"]
        or 0
    )

    return {
        "total_signalements":
            Signalement.objects.count(),

        "total_workorders":
            WorkOrder.objects.count(),

        "total_interventions":
            Intervention.objects.count(),

        "interventions_validees":
            Intervention.objects.filter(
                etat="valide"
            ).count(),

        "pieces_consommees":
            total_pieces,
    }

class DashboardViewSet(viewsets.ViewSet):

    @action(
        detail=False,
        methods=["get"]
    )
    def stats(self, request):

        return Response(
            get_dashboard_stats()
        )