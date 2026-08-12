from maintenance.events.intervention_events import intervention_finished
from maintenance.models import Intervention
from django.utils import timezone
from django.core.exceptions import ValidationError

# 🔹 CREATE
def create_intervention(**validated_data):
    """
    Crée une intervention avec logique métier.
    """
    techniciens = validated_data.pop("techniciens", [])
    workorder = validated_data.pop("workorder", None)
    valide_par = validated_data.pop("valide_par", None)

    intervention = Intervention.objects.create(
        workorder=workorder,
        valide_par=valide_par,
        **validated_data
    )
    if techniciens:
        intervention.techniciens.set(techniciens)
    return intervention


# 🔹 UPDATE
def update_intervention(intervention, **validated_data):
    techniciens = validated_data.pop("techniciens", None)
    for attr, value in validated_data.items():
        setattr(intervention, attr, value)
    intervention.full_clean()
    intervention.save()
    if techniciens is not None:
        intervention.techniciens.set(techniciens)
    return intervention


# 🔹 DELETE
def delete_intervention(intervention):
    intervention.delete()


# 🔹 START
def start_intervention(intervention, user):
    if intervention.date_debut:
        raise ValidationError("Intervention déjà démarrée")

    if getattr(user, "role", None) != "technicien":
        raise ValidationError("Seul un technicien peut démarrer")

    intervention.date_debut = timezone.now()

    # ✅ ajouter le technicien qui démarre si absent
    if not intervention.techniciens.filter(id=user.id).exists():
        intervention.techniciens.add(user)

    intervention.save()
    return intervention


# 🔹 FINISH
def finish_intervention(intervention, user):
    if not intervention.date_debut:
        raise ValidationError("Intervention non démarrée")

    if not intervention.techniciens.filter(id=user.id).exists():
        raise ValidationError("Seul le technicien assigné peut terminer")

    intervention.date_fin = timezone.now()
    intervention.save()

    # Déclenchement d’événement
    intervention_finished(intervention, user)
    return intervention


# 🔹 VALIDATE
def validate_intervention(intervention, user):
    if not intervention.date_fin:
        raise ValidationError("Intervention non terminée")

    if user.role not in ["admin", "expert"]:
        raise ValidationError("Non autorisé à valider")

    intervention.is_locked = True
    intervention.valide_par = user
    intervention.date_validation = timezone.now()
    intervention.save()
    return intervention


# 🔹 LOCK CHECK
def is_intervention_locked(intervention):
    return intervention.is_locked


# 🔹 PERMISSIONS
def can_user_edit_intervention(user, intervention):
    if user.is_superuser:
        return True
    if hasattr(user, "role"):
        if user.role == "admin":
            return True
        if user.role == "technicien" and intervention.techniciens.filter(id=user.id).exists() and not intervention.is_locked:
            return True
    return False
