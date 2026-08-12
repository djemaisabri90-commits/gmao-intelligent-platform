from django.db import transaction
from django.core.exceptions import ValidationError
from maintenance.models import Machine


# 🔹 CREATE
def create_machine(**validated_data):
    """
    Crée une machine avec logique métier éventuelle.
    """
    machine = Machine.objects.create(**validated_data)
    # Synchroniser l'état initial
    machine.update_etat()
    return machine


# 🔹 UPDATE
@transaction.atomic
def update_machine(machine: Machine, data: dict):
    """
    Met à jour une machine et synchronise son état.
    """
    for attr, value in data.items():
        setattr(machine, attr, value)

    machine.save()
    machine.update_etat()
    return machine


# 🔹 DELETE
def delete_machine(machine: Machine):
    """
    Supprime une machine.
    """
    status=machine.etat
    if status != "SERVICE":
        raise ValidationError("Suppression invalide (état)")
    else:
        machine.delete()


# 🔹 CHANGE STATUS (⚠️ réservé aux cas exceptionnels)
def change_machine_status(machine: Machine, status: str):
    """
    Change manuellement le statut de la machine.
    ⚠️ Normalement, l'état est synchronisé via WorkOrders.
    """
    if status not in dict(Machine.STATUS_CHOICES):
        raise ValidationError("Statut invalide")

    machine.etat = status
    machine.save()
    return machine


# 🔹 PERMISSIONS
def can_user_edit_machine(user, machine: Machine):
    """
    Vérifie si l'utilisateur peut modifier une machine.
    """
    if user.is_superuser:
        return True
    if hasattr(user, "role"):
        if user.role == "admin":
            return True
        if user.role == "technicien":
            # Optionnel : autoriser les techniciens à modifier certaines infos
            return True
    return False
