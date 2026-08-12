# maintenance/piece_serializer.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
from maintenance.models import Piece, PieceUtilisee

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        #fields = ["id", "nom", "reference", "stock_disponible", "fournisseur"]
        fields = "__all__"

class PieceUtiliseeSerializer(serializers.ModelSerializer):
    piece_nom = serializers.CharField(source="piece.nom", read_only=True)
    piece_reference = serializers.CharField(source="piece.reference", read_only=True)

    class Meta:
        model = PieceUtilisee
        #fields = ["id", "intervention", "piece", "piece_nom", "piece_reference", "quantite"]
        fields = "__all__"
        
    def validate(self, data):
        piece = data.get("piece")
        quantite = data.get("quantite")

        if quantite is None or quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        if piece and piece.stock_disponible < quantite:
            raise ValidationError("Stock insuffisant pour cette pièce.")
        return data

    def create(self, validated_data):
        piece = validated_data["piece"]
        quantite = validated_data["quantite"]

        # décrémenter le stock
        piece.stock_disponible -= quantite
        piece.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_quantite = validated_data.get("quantite", instance.quantite)
        piece = instance.piece

        # restituer l'ancienne quantité
        piece.stock_disponible += instance.quantite

        if new_quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        if piece.stock_disponible < new_quantite:
            raise ValidationError("Stock insuffisant pour cette pièce.")

        # appliquer la nouvelle quantité
        piece.stock_disponible -= new_quantite
        piece.save()

        instance.quantite = new_quantite
        instance.save()
        return instance
