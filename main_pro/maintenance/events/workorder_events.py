# maintenance/events/workorder_events.py

from maintenance.models import AuditLog


def workorder_created(workorder, user):
    """
    Journalise la création d'un WorkOrder dans l'AuditLog.
    """
    AuditLog.objects.create(
        user=user,
        action="create",  # ✅ cohérent avec ACTIONS définis dans AuditLog
        model="WorkOrder",  # ✅ champ correct
        object_id=workorder.id
    )


def workorder_updated(workorder, user, changements=None):
    """
    Journalise la mise à jour d'un WorkOrder.
    """
    AuditLog.objects.create(
        user=user,
        action="update",
        model="WorkOrder",
        object_id=workorder.id,
        changements=changements or {}
    )


def workorder_deleted(workorder, user):
    """
    Journalise la suppression d'un WorkOrder.
    """
    AuditLog.objects.create(
        user=user,
        action="delete",
        model="WorkOrder",
        object_id=workorder.id
    )
