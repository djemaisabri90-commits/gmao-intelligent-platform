from django.db import models
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from maintenance.models import Intervention, Piece, PieceUtilisee
from maintenance.serializers.intervention_serializer import (
    InterventionWriteSerializer,
    InterventionReadSerializer
)
from maintenance.selectors.intervention_selectors import (
    get_interventions,
    get_intervention_stats
)
from maintenance.services.intervention_service import (
    create_intervention,
    update_intervention,
    delete_intervention,
    start_intervention,
    finish_intervention,
    validate_intervention,
    is_intervention_locked
)
from maintenance.services.audit_service import audit_action, get_audit_changes
from maintenance.base.permissions import InterventionPermission


class InterventionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated, InterventionPermission]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrer les interventions selon le rôle utilisateur"""
        user = self.request.user
        qs = get_interventions()
        #qs = Intervention.objects.all()
        role = getattr(user, "role", None)

        if role in ["admin", "expert"]:
            return qs
        
        if role == "technicien":
            # ✅ filtrer sur ManyToMany
            #return qs.filter(workorder__techniciens=user)
            return qs.filter(
                models.Q(workorder__techniciens=user) |
                models.Q(techniciens=user) |
                models.Q(workorder__interventions__techniciens=user)
            ).distinct()
        
        return qs.none()

    def get_serializer_class(self):
        """Choisir le serializer selon l’action"""
        if self.action in ["list", "retrieve", "statistiques", "start", "finish", "validate"]:
            return InterventionReadSerializer
        return InterventionWriteSerializer

    def get_object(self):
        """Sécuriser l’accès aux objets selon rôle"""
        obj = super().get_object()
        user = self.request.user
        role = getattr(user, "role", None)

        if role in ["admin", "expert"]:
            return obj
        if role == "technicien" and (
            obj.workorder.techniciens.filter(id=user.id).exists() or
            obj.techniciens.filter(id=user.id).exists()
        ):
            return obj
        """
        if role == "expert" and obj.etat in ["termine", "valide"]:
            return obj
        """

        raise PermissionDenied("Accès refusé")

    def perform_create(self, serializer):
        """Créer une intervention via service + audit"""
        instance = create_intervention(**serializer.validated_data)
        audit_action(self.request, "create", instance)
        serializer.instance = instance

    def perform_update(self, serializer):
        """Bloquer modification si intervention verrouillée"""
        intervention = self.get_object()
        if is_intervention_locked(intervention):
            raise PermissionDenied("Intervention verrouillée")

        old_instance = intervention
        new_data = serializer.validated_data
        changements = get_audit_changes(old_instance, new_data)

        instance = update_intervention(intervention, new_data)
        audit_action(self.request, "update", instance, changements)
        serializer.instance = instance

    def perform_destroy(self, instance):
        """Bloquer suppression si intervention verrouillée"""
        if is_intervention_locked(instance):
            raise PermissionDenied("Intervention verrouillée")
        audit_action(self.request, "delete", instance)
        delete_intervention(instance)

    # --- Actions métier ---

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        intervention = self.get_object()

        pieces = request.data.get("pieces", [])
        # Réservation des pièces
        for item in pieces:

            piece = Piece.objects.get(
                pk=item["piece_id"]
            )
            PieceUtilisee.objects.create(
                intervention=intervention,
                piece=piece,
                quantite=item["quantite"],
                etat="reservee"
            )


        start_intervention(intervention, request.user)
        audit_action(request, "start", intervention)
        return Response(InterventionReadSerializer(intervention).data)

    @action(detail=True, methods=["post"])
    def finish(self, request, pk=None):
        intervention = self.get_object()
        finish_intervention(intervention, request.user)
        audit_action(request, "finish", intervention)
        return Response(InterventionReadSerializer(intervention).data)

    @action(detail=True, methods=["post"])
    def validate(self, request, pk=None):
        intervention = self.get_object()
        validate_intervention(intervention, request.user)
        audit_action(request, "validate", intervention)
        return Response(InterventionReadSerializer(intervention).data)

    @action(detail=False, methods=["get"], url_path="statistiques")
    def statistiques(self, request):
        """Endpoint pour statistiques globales"""
        stats = get_intervention_stats(user=request.user)
        # ✅ Normaliser les clés pour correspondre au frontend
        response_data = {
            "en_attente": stats["by_etat"].get("en_attente", 0),
            "en_cours": stats["by_etat"].get("en_cours", 0),
            "termine": stats["by_etat"].get("termine", 0),
            "valide": stats["by_etat"].get("valide", 0),
            "total": stats["total"],
            "by_priority": stats["by_priority"],
            "by_type": stats["by_type"],
            "avg_duration": stats["avg_duration"],
        }
        return Response(response_data)
    
    @action(detail=True, methods=["post"])
    def start_with_pieces(self, request, pk=None):

        intervention = self.get_object()

        pieces = request.data.get("pieces", [])

        for item in pieces:

            piece = Piece.objects.get(
            id=item["piece_id"]
            )

            PieceUtilisee.objects.create(
                intervention=intervention,
                piece=piece,
                quantite=item["quantite"],
                etat="reservee"
            )

            intervention.etat = "en_cours"
            intervention.date_debut = timezone.now()
            intervention.save()

        return Response(
        {"message": "Intervention démarrée"}
        )
