# maintenance/views/piece_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from maintenance.base.permissions import IsAdminOrExpert
from maintenance.serializers.piece_serializer import PieceSerializer
from maintenance.selectors.piece_selectors import get_pieces
from maintenance.services.piece_service import create_piece, update_piece, delete_piece
from maintenance.models import Piece

class PieceViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les pièces (stock global).
    Utilise les services pour encapsuler la logique métier.
    """
    serializer_class = PieceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_pieces()

    def perform_create(self, serializer):
        create_piece(serializer.validated_data)

    def perform_update(self, serializer):
        piece = self.get_object()
        update_piece(piece, serializer.validated_data)

    def perform_destroy(self, instance: Piece):
        delete_piece(instance)
