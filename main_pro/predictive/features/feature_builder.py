# predictive/features/feature_builder.py

from django.db.models import Sum, Prefetch
from django.utils import timezone
from datetime import timedelta
from maintenance.models import Machine, Intervention, WorkOrder, PieceUtilisee, Notification

def build_features():
    dataset = []
    now = timezone.now()

    machines = Machine.objects.prefetch_related(
        "workorder_set__interventions__pieces",   # ✅ grâce à related_name="pieces"
        "workorder_set__notifications",
        "workorder_set__interventions"            # interventions préchargées
    )

    for machine in machines:
        dataset.append(_extract_features(machine, now))

    return dataset

def build_features_for_machine(machine):
    now = timezone.now()
    return _extract_features(machine, now)

def _extract_features(machine, now):
    workorders = machine.workorder_set.all()
    interventions = Intervention.objects.filter(workorder__machine=machine)
    notifications = Notification.objects.filter(workorder__machine=machine)

    # Utilisation de la propriété Python `etat`
    workorders_en_cours = sum(
        1 for wo in workorders
        if any(i.etat in ["en_attente", "en_cours", "termine"] for i in wo.interventions.all())
    )

    workorders_clos = sum(
        1 for wo in workorders
        if wo.interventions.exists() and all(i.etat == "valide" for i in wo.interventions.all())
    )

    # ✅ pièces déjà préchargées via related_name="pieces"
    all_pieces = [p for wo in workorders for i in wo.interventions.all() for p in i.pieces.all()]

    features = {
        "machine_id": machine.id,
        "total_interventions": interventions.count(),
        "validated_interventions": sum(1 for i in interventions if i.date_validation is not None),
        "pending_interventions": sum(1 for i in interventions if i.date_debut is None),
        "recent_interventions": sum(1 for i in interventions if i.date_debut and i.date_debut >= now - timedelta(days=30)),
        "total_workorders": workorders.count(),
        "high_priority_workorders": workorders.filter(priorite="high").count(),
        "workorders_en_cours": workorders_en_cours,
        "workorders_clos": workorders_clos,
        "total_pieces_used": sum(p.quantite for p in all_pieces),
        "stock_critique": 1 if any(p.piece.stock_disponible < 5 for p in all_pieces) else 0,
        "recent_notifications": notifications.filter(created_at__gte=now - timedelta(days=30)).count(),
        "is_in_failure": 1 if machine.etat == "PANNE" else 0,
    }

    features["target"] = 1 if (
        features["recent_interventions"] > 2 or
        features["stock_critique"] == 1 or
        features["recent_notifications"] > 5 or
        features["workorders_en_cours"] > 0
    ) else 0

    return features
