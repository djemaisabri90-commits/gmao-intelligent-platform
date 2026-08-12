"""
test complet qu'utilise
la fonction notify_technicien(intervention)
pour valider
la __réassignation__ et la __notification__ 
lancer directement avec pytest.
pytest maintenance/test_workflow2.py

#explications
Explications
On crée deux techniciens (tech1, tech2).

Le WorkOrder est d’abord assigné à tech1.

L’admin le réassigne à tech2.

L’intervention est mise à jour avec le nouveau technicien.

On mock async_to_sync(channel_layer.group_send)
pour capturer la notification.

On vérifie que la notification est bien envoyée
au groupe technicien_{tech2.id}
avec les bonnes infos.
"""

#ce que j'ai validé
"""
✅ Création d’un WorkOrder avec technicien.

✅ Création d’une intervention liée.

✅ Réassignation vers un autre technicien.

✅ Notification envoyée au bon groupe WebSocket.

✅ Test exécuté avec succès via pytest et Django.
"""

import pytest
from django.utils import timezone
from maintenance.models import Machine
from maintenance.services.workorder_services import create_workorder
from maintenance.services.intervention_service import create_intervention, notify_technicien
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_reassignation_technicien(monkeypatch):
    admin = User.objects.create(username="admin", role="admin")
    tech1 = User.objects.create(username="tech1", role="technicien")
    tech2 = User.objects.create(username="tech2", role="technicien")

    machine = Machine.objects.create(nom="Machine Test", description="Machine de test")

    # Étape 1 : Création WorkOrder avec technicien 1
    workorder = create_workorder(
        machine=machine,
        description="WorkOrder avec technicien 1",
        technicien=tech1,
        cree_par=admin
    )

    intervention = create_intervention(
        workorder=workorder,
        technicien=tech1,
        type_intervention="corrective",
        priorite="haute",
        statut="en_attente"
    )

    assert intervention.technicien == tech1

    # Étape 2 : Réassignation vers technicien 2
    workorder.technicien = tech2
    workorder.save()

    intervention.technicien = tech2
    intervention.full_clean()
    intervention.save()

    assert intervention.technicien == tech2

    # Étape 3 : Mock notification
    notified = {}
    def fake_notify(group, message):
        notified["group"] = group
        notified["message"] = message

    monkeypatch.setattr(
        "maintenance.services.intervention_service.async_to_sync",
        lambda f: lambda *args, **kwargs: fake_notify(args[0], args[1])
    )

    # Appel de la fonction de notification
    notify_technicien(intervention)

    # Vérification que la notification est envoyée au bon technicien
    assert notified["group"] == f"technicien_{tech2.id}"
    assert notified["message"]["message"]["id"] == intervention.id
    assert notified["message"]["message"]["workorder"] == workorder.id
    assert notified["message"]["message"]["statut"] == intervention.statut
