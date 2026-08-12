import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, Signalement,
    WorkOrder, Intervention, Piece, PieceUtilisee, Notification
)

@pytest.mark.django_db
report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

# 🔎 Vérification rapide
import json
print(json.dumps(report, indent=2))

validation_results = report

TrainingLog.objects.create(
    dataset_size=len(df),
    class_distribution=sanitize_for_json(initial_distribution),
    balanced_distribution=sanitize_for_json(balanced_distribution),
    accuracy=round(report["accuracy"], 3),
    precision=round(report["weighted avg"]["precision"], 3),
    recall=round(report["weighted avg"]["recall"], 3),
    f1_score=round(report["weighted avg"]["f1-score"], 3),
    user=user,
    success=True,
    validation_metrics=sanitize_for_json(validation_results),  # ✅ rapport complet
    confusion_matrix=cm,
    balanced_accuracy=round(balanced_acc, 3),
    macro_f1=round(report["macro avg"]["f1-score"], 3),
    minority_ratio=minority_ratio,
    hyperparameters=sanitize_for_json(best_params)
)
