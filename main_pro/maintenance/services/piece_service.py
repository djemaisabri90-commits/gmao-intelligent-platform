# src/pieces/services/piece_service.py
from django.core.exceptions import ObjectDoesNotExist
from maintenance.models import Piece

def create_piece(data: dict) -> Piece:
    """
    Crée une nouvelle pièce.
    """
    return Piece.objects.create(**data)

def update_piece(piece: Piece, data: dict) -> Piece:
    """
    Met à jour une pièce existante avec les données fournies.
    """
    for attr, value in data.items():
        if hasattr(piece, attr):
            setattr(piece, attr, value)
    piece.save()
    return piece

def delete_piece(piece: Piece) -> None:
    """
    Supprime une pièce.
    """
    piece.delete()

def get_piece_by_id(piece_id: int) -> Piece:
    """
    Récupère une pièce par son ID.
    """
    try:
        return Piece.objects.get(id=piece_id)
    except ObjectDoesNotExist:
        return None
