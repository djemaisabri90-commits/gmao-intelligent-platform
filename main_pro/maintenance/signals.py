import random
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Intervention, WorkOrder, Notification, Signalement, Machine

from django.contrib.auth import get_user_model
Utilisateur = get_user_model()

def generate_random_password(length=8):
    """Génère un mot de passe temporaire lisible (sans caractères ambigus comme I, O, 0, 1)"""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789@"
    return "".join(random.choices(chars, k=length))

# 🤖 AUTOMATISATION : Signal Django pour générer le code dès la création du compte
@receiver(post_save, sender=Utilisateur)
def generate_activation_token(sender, instance, created, **kwargs):

    if not created:
        return

    update_fields = []

    # Génération du code d'activation
    if not instance.activation_token:
        instance.activation_token = "".join(
            random.choices(
                "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
                k=6
            )
        )
        update_fields.append("activation_token")

    # Génération du mot de passe temporaire
    if instance.password.startswith("!"):
        temp_password = generate_random_password()

        # Conserver temporairement le mot de passe en clair
        instance.temporary_password = temp_password

        instance._temp_password_plain = temp_password


        # Hash sécurisé
        instance.set_password(temp_password)

        update_fields.append("password")

    # Sauvegarde unique
    if update_fields:
        instance.save(update_fields=update_fields)

        # 💡 Astuce PFE : On peut stocker temporairement le mot de passe en clair dans un attribut 
            # non persistant (non sauvegardé en BDD) pour que le serializer puisse le renvoyer UNIQUEMENT 
            # lors de la réponse de création à l'admin.


# --- Signalement ---
@receiver(post_save, sender=Signalement)
def maj_machine_etat_signalement(sender, instance, created, **kwargs):
    """
    Dès qu'un signalement est créé, la machine associée passe en état 'PANNE'.
    """
    if created and instance.machine:
        instance.machine.etat = "PANNE"
        instance.machine.save()

# --- Intervention ---
@receiver(post_save, sender=Intervention)
def maj_machine_etat_intervention(sender, instance, **kwargs):
    """
    Met à jour l'état de la machine en fonction de l'intervention.
    """
    machine = instance.workorder.machine

    # Intervention démarrée mais pas encore validée
    if instance.date_debut and not instance.date_validation:
        machine.etat = "MAINTENANCE"
        machine.save()

    # Intervention validée par expert/admin
    elif instance.date_validation and instance.valide_par and instance.is_locked:
        machine.etat = "SERVICE"
        machine.save()

# --- WorkOrder ---
@receiver(post_save, sender=Intervention)
def update_workorder_etat(sender, instance, **kwargs):
    """
    Vérifie si toutes les interventions d'un WorkOrder sont validées.
    Si oui, clôture automatique du WorkOrder et notification.
    """

    wo = instance.workorder

    # Vérifier si toutes les interventions sont validées
    if all(i.etat == "valide" for i in wo.interventions.all()):
        
        # ✅ Clôture automatique
        if not wo.date_cloture:
            wo.date_cloture = timezone.now()
            wo.save()

            # ✅ Mise à jour de l'état de la machine
            wo.machine.etat = "SERVICE"
            wo.machine.save()

            # ✅ Notification au créateur du WorkOrder
            Notification.objects.create(
                user=wo.cree_par,
                message=f"WorkOrder #{wo.id} clôturé automatiquement",
                type=Notification.NotificationType.WORKORDER_CREATED,
                workorder=wo
            )

