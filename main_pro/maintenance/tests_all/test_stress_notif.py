import pytest
from django.utils import timezone
from maintenance.models import Utilisateur, Notification, WorkOrder, Machine

@pytest.mark.django_db
def test_stress_notifications_pagination_persistance():
    user = Utilisateur.objects.create(username="op1", role="operateur")
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    machine = Machine.objects.create(nom="Machine Stress Notifications", etat="SERVICE")

    wo = WorkOrder.objects.create(
        description="WO Stress Notifications",
        cree_par=expert,
        expert=expert,
        machine=machine
    )

    # Génération de 200 notifications
    for i in range(200):
        Notification.objects.create(
            user=user,
            message=f"Notification {i+1}",
            type=Notification.NotificationType.WORKORDER_CREATED,
            workorder=wo
        )

    # Vérifier que toutes les notifications sont persistées
    assert Notification.objects.filter(user=user).count() == 200

    # Page 1 → 50 notifications
    page1 = Notification.objects.filter(user=user).order_by("-created_at")[:50]
    assert len(page1) == 50

    # Vérifier que l’ordre est décroissant
    created_times = [n.created_at for n in page1]
    assert all(created_times[i] >= created_times[i+1] for i in range(len(created_times)-1))

    # Page 2 → notifications suivantes
    page2 = Notification.objects.filter(user=user).order_by("-created_at")[50:100]
    assert len(page2) == 50

    # ✅ Suppression partielle (récupérer puis delete)
    to_delete = Notification.objects.filter(user=user).order_by("-created_at")[:10]
    for notif in to_delete:
        notif.delete()

    remaining = Notification.objects.filter(user=user).count()
    assert remaining == 190
