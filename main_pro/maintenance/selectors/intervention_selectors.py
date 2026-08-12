# maintenance/selectors/intervention_selectors.py
from maintenance.models import Intervention
from django.db.models import Count, Avg, ExpressionWrapper, F, DurationField
from django.db.models import Prefetch

def get_intervention_queryset(with_relations=True):
    qs = Intervention.objects.all()
    if with_relations:
        qs = qs.select_related(
            "workorder",
            "workorder__machine",
            "workorder__expert",
            "workorder__cree_par",
            "valide_par",
        ).prefetch_related(
            "workorder__techniciens",
            "techniciens"
        )
    return qs

def get_interventions(filters=None, user=None, with_relations=True):
    qs = get_intervention_queryset(with_relations)
    if filters:
        qs = qs.filter(**filters)
    if user and not user.is_superuser:
        if hasattr(user, "role"):
            if user.role == "technicien":
                qs = qs.filter(techniciens=user)  # ✅ ManyToMany
            elif user.role == "expert":
                #qs = qs.filter(valide_par=user)
                pass
    return qs.order_by("-created_at")

def get_intervention_detail(intervention_id, with_relations=True):
    qs = get_intervention_queryset(with_relations)
    return qs.get(id=intervention_id)

def get_interventions_by_workorder(workorder_id):
    return get_intervention_queryset().filter(workorder_id=workorder_id)

def get_intervention_stats(user=None):
    qs = Intervention.objects.all()
    if user and not user.is_superuser:
        if hasattr(user, "role"):
            if user.role == "technicien":
                qs = qs.filter(techniciens=user)  # ✅ ManyToMany
            elif user.role == "expert":
                #qs = qs.filter(valide_par=user)
                pass

    # Stats par état (calculés en Python car etat est une propriété)
    by_etat = {"en_attente": 0, "en_cours": 0, "termine": 0, "valide": 0, "clos": 0}
    for interv in qs:
        by_etat[interv.etat] = by_etat.get(interv.etat, 0) + 1

    # Stats par priorité
    by_priority = dict(qs.values("priorite").annotate(count=Count("id")).values_list("priorite", "count"))

    # Stats par type d’intervention
    by_type = dict(qs.values("type_intervention").annotate(count=Count("id")).values_list("type_intervention", "count"))

    # Durée moyenne des interventions terminées
    closed = qs.filter(date_debut__isnull=False, date_fin__isnull=False)
    avg_duration = None
    if closed.exists():
        delta = ExpressionWrapper(F("date_fin") - F("date_debut"), output_field=DurationField())
        avg_delta = closed.annotate(delta=delta).aggregate(avg=Avg("delta"))["avg"]
        if avg_delta:
            avg_duration = avg_delta.total_seconds() / 3600  # en heures

    stats = {
        "total": qs.count(),
        "by_etat": by_etat,
        "by_priority": by_priority,
        "by_type": by_type,
        "avg_duration": avg_duration,
        "pending_count": by_etat.get("en_attente", 0),
    }

    return stats
