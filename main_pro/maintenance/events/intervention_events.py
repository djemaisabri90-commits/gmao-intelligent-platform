# maintenance/events/intervention_events.py

from maintenance.models import Log
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def _notify_channel(group_name: str, message: dict):
    """
    Envoie une notification via WebSocket au groupe spécifié.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "intervention.notification",
            "message": message,
        }
    )


def intervention_started(intervention, user):
    """
    Journalise et notifie le démarrage d'une intervention.
    """
    Log.objects.create(
        workorder=intervention.workorder,
        machine=intervention.workorder.machine,
        user=user,
        action=f"Intervention #{intervention.id} démarrée",
        etat_intervention=intervention.etat
    )
    for technicien in intervention.techniciens.all():
        _notify_channel(
            f"technicien_{technicien.id}",
            {
                "id": intervention.id,
                "workorder": intervention.workorder.id,
                "machine": intervention.workorder.machine.nom,
                "etat": intervention.etat,
                "message": "Intervention démarrée",
            }
        )


def intervention_finished(intervention, user):
    """
    Journalise et notifie la fin d'une intervention.
    """
    Log.objects.create(
        workorder=intervention.workorder,
        machine=intervention.workorder.machine,
        user=user,
        action=f"Intervention #{intervention.id} terminée",
        etat_intervention=intervention.etat,
        metadata={"duration": (intervention.date_fin - intervention.date_debut).total_seconds()}
    )
    for technicien in intervention.techniciens.all():
        _notify_channel(
            f"technicien_{technicien.id}",
            {
                "id": intervention.id,
                "workorder": intervention.workorder.id,
                "machine": intervention.workorder.machine.nom,
                "etat": intervention.etat,
                "message": "Intervention terminée",
            }
        )


def intervention_validated(intervention, user):
    """
    Journalise et notifie la validation d'une intervention.
    """
    Log.objects.create(
        workorder=intervention.workorder,
        machine=intervention.workorder.machine,
        user=user,
        action=f"Intervention #{intervention.id} validée par {user.username}",
        etat_intervention=intervention.etat
    )
    for technicien in intervention.techniciens.all():
        _notify_channel(
            f"technicien_{technicien.id}",
            {
                "id": intervention.id,
                "workorder": intervention.workorder.id,
                "machine": intervention.workorder.machine.nom,
                "etat": intervention.etat,
                "message": "Intervention validée",
            }
        )
