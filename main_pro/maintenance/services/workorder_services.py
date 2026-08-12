# maintenance/services/workorder_service.py
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from maintenance.models import WorkOrder
from maintenance.services.intervention_service import create_intervention

PRIORITE_MAPPING = {
    'low': 'basse',
    'medium': 'moyenne',
    'high': 'haute',
}

TYPE_MAPPING = {
    'corrective': 'Corrective',
    'preventive': 'Préventive',
    'inspection': 'Inspection',
}

def create_workorder(
    machine,
    categorie,
    description,
    type="predictive",
    priorite="high",
    signalement=None,
    techniciens=None,
    expert=None,
    cree_par=None,
    date_cloture=None,
):
    """
    Crée un bon de travail.
    - La source est automatiquement héritée du signalement si présent.
    - Si un technicien est assigné, une intervention est automatiquement créée.
    """
    workorder = WorkOrder(
        machine=machine,
        categorie=categorie,
        description=description,
        type=type,
        priorite=priorite,
        signalement=signalement,
        expert=expert,
        cree_par=cree_par,
        date_cloture=date_cloture,
    )

    workorder.full_clean()
    workorder.save()

    # Création automatique de l'intervention si un technicien est assigné
    if techniciens:
        workorder.techniciens.set(techniciens)
        priorite_intervention = PRIORITE_MAPPING.get(workorder.priorite, 'moyenne')
        #for t in workorder.techniciens.all():
        create_intervention(
                workorder=workorder,
                techniciens=list(workorder.techniciens.all()),
                type_intervention="inspection",
                priorite=priorite_intervention,
                actions_realisees="",
            )

    return workorder


@transaction.atomic
def update_workorder(workorder, data):
    """
    Met à jour un bon de travail.
    """
    for field in [
        "type",
        "priorite",
        "description",
        "expert",
        "signalement",
    ]:
        if field in data:
            workorder.techniciens.set(data["techniciens"])

    # Gestion de la date_cloture si fournie
    if "date_cloture" in data:
        workorder.date_cloture = data["date_cloture"]

    workorder.full_clean()
    workorder.save()
    return workorder


def delete_workorder(workorder):
    """Supprime un bon de travail."""
    workorder.delete()


def can_user_edit_workorder(user, workorder):
    """
    Vérifie si l'utilisateur a le droit de modifier ce bon de travail.
    """
    if user.is_superuser:
        return True
    if hasattr(user, 'role'):
        if user.role == "admin":
            return True
        if user.role == "expert" and workorder.expert == user:
            return True
        if user.role == "technicien" and workorder.techniciens == user:
            return True
    return False


def assign_technician(workorder, techniciens):
    """Assigne un ou plusieurs techniciens au bon de travail."""
    workorder.techniciens.set(techniciens)
    workorder.full_clean()
    workorder.save()
    return workorder


def assign_expert(workorder, expert):
    """Assigne un expert au bon de travail."""
    workorder.expert = expert
    workorder.full_clean()
    workorder.save()
    return workorder
