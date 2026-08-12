# src/pieces/services/piece_utilisee_service.py
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from maintenance.models import Piece, PieceUtilisee

def create_piece_utilisee(intervention, piece_id: int, quantite: int) -> PieceUtilisee:
    """
    Crée une pièce utilisée pour une intervention donnée.
    Décrémente automatiquement le stock de la pièce.
    """
    try:
        piece = Piece.objects.get(id=piece_id)
    except ObjectDoesNotExist:
        raise ValidationError("La pièce spécifiée n'existe pas.")

    if quantite <= 0:
        raise ValidationError("La quantité doit être positive.")
    if piece.stock_disponible < quantite:
        raise ValidationError("Stock insuffisant pour cette pièce.")

    piece_utilisee = PieceUtilisee.objects.create(
        intervention=intervention,
        piece=piece,
        quantite=quantite
    )
    return piece_utilisee

def update_piece_utilisee(piece_utilisee: PieceUtilisee, quantite: int) -> PieceUtilisee:
    """
    Met à jour la quantité d'une pièce utilisée.
    Ajuste le stock en conséquence.
    """
    if quantite <= 0:
        raise ValidationError("La quantité doit être positive.")

    # recalcul du stock : restituer l'ancienne quantité puis décrémenter la nouvelle
    piece = piece_utilisee.piece
    piece.stock_disponible += piece_utilisee.quantite  # restituer
    if piece.stock_disponible < quantite:
        raise ValidationError("Stock insuffisant pour cette pièce.")

    piece_utilisee.quantite = quantite
    piece_utilisee.save()
    return piece_utilisee

def delete_piece_utilisee(piece_utilisee: PieceUtilisee) -> None:
    """
    Supprime une pièce utilisée et restitue le stock.
    """
    piece = piece_utilisee.piece
    piece.stock_disponible += piece_utilisee.quantite
    piece.save()
    piece_utilisee.delete()
