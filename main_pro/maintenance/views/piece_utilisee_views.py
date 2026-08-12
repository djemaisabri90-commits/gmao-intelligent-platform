# maintenance/views/piece_utilisee_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal

from maintenance.serializers.piece_serializer import PieceUtiliseeSerializer
from maintenance.models import Intervention, PieceUtilisee
from maintenance.services.piece_utilisee_service import (
    create_piece_utilisee,
    update_piece_utilisee,
    delete_piece_utilisee,
)

class PieceUtiliseeViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les pièces utilisées (liées aux interventions).
    Décrémentation/restauration du stock gérée via services.
    """
    serializer_class = PieceUtiliseeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PieceUtilisee.objects.all()

    def perform_create(self, serializer):
        intervention = serializer.validated_data["intervention"]
        piece_id = serializer.validated_data["piece"].id
        quantite = serializer.validated_data["quantite"]
        create_piece_utilisee(intervention, piece_id, quantite)

    def perform_update(self, serializer):
        piece_utilisee = self.get_object()
        quantite = serializer.validated_data.get("quantite", piece_utilisee.quantite)
        update_piece_utilisee(piece_utilisee, quantite)

    def perform_destroy(self, instance: PieceUtilisee):
        delete_piece_utilisee(instance)






    def total_piece():
        total_pieces = (PieceUtilisee.objects.aggregate(
                total=Sum("quantite"))["total"] or 0)

        return {
            "pieces_consommees":
            total_pieces,
        }

    @action(detail=False, methods=["get"])
    def total(self, request):
        return Response(
            self.total_piece()
        )
    

    def cout_piece(self):

        total_quantite = 0
        total_cout = Decimal("0")

        for ligne in PieceUtilisee.objects.select_related("piece"):
            total_quantite += ligne.quantite
            total_cout += ligne.quantite * ligne.piece.prix_unitaire

        return {
            "pieces_consommees": total_quantite,
            "cout_total_pieces": total_cout,
        }
    @action(detail=False, methods=["get"])
    def cout(self, request):
        return Response(self.cout_piece())
    
    @action(detail=False, methods=["get"])
    def cout_par_intervention(self, request):

        data = []

        interventions = Intervention.objects.prefetch_related(
        "pieces__piece"
        )

        for intervention in interventions:

            total = 0

            for ligne in intervention.pieces.all():
                total += ligne.quantite * ligne.piece.prix_unitaire

            data.append({
                "intervention_id": intervention.id,
                "cout_total": total,
            })

        return Response(data)
    
    @action(detail=False, methods=["get"])
    def statistiques(self, request):

        pieces_consommees = (
            PieceUtilisee.objects.aggregate(
            total=Sum("quantite")
            )["total"] or 0
        )

        cout_total_pieces = sum(
            ligne.cout_total
            for ligne in PieceUtilisee.objects.select_related("piece")
        )

        couts_interventions = []

        interventions = Intervention.objects.prefetch_related(
            "pieces__piece"
        )

        for intervention in interventions:
            couts_interventions.append({
                "intervention_id": intervention.id,
                "cout_total": float(intervention.cout_pieces)
            })

        intervention_plus_couteuse = None
        intervention_moins_couteuse = None
        cout_moyen = 0

        if couts_interventions:

            intervention_plus_couteuse = max(
                couts_interventions,
                key=lambda x: x["cout_total"]
            )

            intervention_moins_couteuse = min(
                couts_interventions,
                key=lambda x: x["cout_total"]
            )

            cout_moyen = (
                sum(x["cout_total"] for x in couts_interventions)
                / len(couts_interventions)
            )

        return Response({
            "pieces_consommees": pieces_consommees,
            "cout_total_pieces": float(cout_total_pieces),

            "cout_moyen_intervention": round(cout_moyen, 3),

            "intervention_plus_couteuse":
                intervention_plus_couteuse,

            "intervention_moins_couteuse":
                intervention_moins_couteuse,

            "cout_par_intervention":
                couts_interventions
        })

"""    
    @action(detail=False, methods=["get"])
    def statistiques(self, request):

        interventions = Intervention.objects.prefetch_related(
        "pieces__piece"
        )

        return Response({
            "pieces_consommees": PieceUtilisee.objects.aggregate(
            total=Sum("quantite")
            )["total"] or 0,

            "cout_total_pieces": sum(
            ligne.cout_total
            for ligne in PieceUtilisee.objects.select_related("piece")
            ),

            "cout_par_intervention": [
                {
                "intervention_id": i.id,
                "cout_total": i.cout_pieces,
                }
                for i in interventions
            ]
        })
    


@action(detail=False, methods=["get"])
def statistiques(self, request):

    pieces_consommees = (
        PieceUtilisee.objects.aggregate(
            total=Sum("quantite")
        )["total"]
        or 0
    )

    cout_total = Decimal("0")

    for ligne in PieceUtilisee.objects.select_related("piece"):
        cout_total += (
            ligne.quantite *
            ligne.piece.prix_unitaire
        )

    cout_par_intervention = []

    interventions = Intervention.objects.prefetch_related(
        "pieces__piece"
    )

    for intervention in interventions:

        total_intervention = Decimal("0")

        for ligne in intervention.pieces.all():
            total_intervention += (
                ligne.quantite *
                ligne.piece.prix_unitaire
            )

        cout_par_intervention.append({
            "intervention_id": intervention.id,
            "cout_total": total_intervention,
        })

    return Response({
        "pieces_consommees": pieces_consommees,
        "cout_total_pieces": cout_total,
        "cout_par_intervention": cout_par_intervention,
    })


@action(detail=False, methods=["get"])
def statistiques(self, request):

    interventions = Intervention.objects.all()

    cout_total = sum(
        intervention.cout_pieces
        for intervention in interventions
    )

    return Response({
        "pieces_consommees":
            PieceUtilisee.objects.count(),

        "cout_total_pieces":
            cout_total,

        "cout_par_intervention": [
            {
                "intervention_id": intervention.id,
                "cout_total": intervention.cout_pieces,
            }
            for intervention in interventions
        ]
    })
"""

