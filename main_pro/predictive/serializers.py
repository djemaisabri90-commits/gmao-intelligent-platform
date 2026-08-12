# predictive/serializers.py

from rest_framework import serializers
from predictive.models import TrainingLog

class TrainingLogSerializer(serializers.ModelSerializer):
    # format personnalisé : jour/mois/année heure:minute
    trained_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    user = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  # ✅ champ calculé
    class Meta:
        model = TrainingLog
        fields = [
            "model_version",
            "trained_at",
            "user",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "dataset_size",
            "class_distribution",
            "balanced_distribution",
            "success",
            "status",
            "validation_metrics",
            "confusion_matrix",
            "balanced_accuracy",
            "macro_f1",
            "minority_ratio",
            "hyperparameters",         
        ]
    
    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "username": obj.user.username
            }
        return None
    
    def get_status(self, obj):
        return "success" if obj.success else "failed"
