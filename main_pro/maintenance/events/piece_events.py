# maintenance/events/piece_events.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from maintenance.models import Piece
from maintenance.services.audit_service import audit_action


@receiver(post_save, sender=Piece)
def piece_saved(sender, instance, created, **kwargs):
    """
    Journalise la création ou la mise à jour d'une pièce.
    """
    action = "create" if created else "update"

    audit_action(
        request=None,  # pas de requête directe, donc user=None
        action=action,
        instance=instance,
        changements=None
    )


@receiver(post_delete, sender=Piece)
def piece_deleted(sender, instance, **kwargs):
    """
    Journalise la suppression d'une pièce.
    """
    audit_action(
        request=None,
        action="delete",
        instance=instance,
        changements=None
    )
