# predictive/models.py

from django.db import models
from django.utils import timezone
from django.conf import settings

class TrainingLog(models.Model):
    trained_at = models.DateTimeField(default=timezone.now, db_index=True)
    dataset_size = models.IntegerField()
    class_distribution = models.JSONField() # ✅ avant équilibrage
    balanced_distribution = models.JSONField(null=True, blank=True)  # ✅ après équilibrage
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()

    # 🔒 qui a lancé l'entraînement
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_logs"
    )

    # 📈 version du modèle
    model_version = models.PositiveIntegerField(default=1)

    success = models.BooleanField(default=True)

    # ➕ nouveau champ pour stocker les métriques de validation externe
    validation_metrics = models.JSONField(null=True, blank=True)
    confusion_matrix = models.JSONField(null=True, blank=True)
    balanced_accuracy = models.FloatField(null=True, blank=True)
    macro_f1 = models.FloatField(null=True, blank=True)

    minority_ratio = models.FloatField(default=0.2)

    # ✅ Nouveau champ pour stocker les hyperparamètres
    hyperparameters = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # nouveau log
            last_version = TrainingLog.objects.aggregate(models.Max("model_version"))["model_version__max"]
            self.model_version = (last_version or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Model v{self.model_version} - {self.trained_at:%Y-%m-%d %H:%M} (acc {self.accuracy})"
