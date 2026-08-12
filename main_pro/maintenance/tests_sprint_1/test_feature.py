# tests/test_feature_builder.py
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from maintenance.models import Machine, WorkOrder, Intervention, Piece, PieceUtilisee, Notification
from predictive.features.feature_builder import build_features_for_machine

User = get_user_model()

@pytest.mark.django_db
def test_build_features_for_machine():
    User = get_user_model()
    user = User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="testpassword",
        role="admin"
    )

    machine = Machine.objects.create(nom="Machine A", etat="SERVICE")

    wo = WorkOrder.objects.create(
        machine=machine,
        priorite="high",
        description="Test WorkOrder",
        cree_par=user
    )

    intervention = Intervention.objects.create(workorder=wo, date_debut=timezone.now())

    piece = Piece.objects.create(nom="Roulement", stock_disponible=10)
    PieceUtilisee.objects.create(intervention=intervention, piece=piece, quantite=3)

    Notification.objects.create(workorder=wo, created_at=timezone.now())

    features = build_features_for_machine(machine)

    assert features["machine_id"] == machine.id
    assert features["total_interventions"] == 1
    assert features["total_workorders"] == 1
    assert features["total_pieces_used"] == 3
    assert features["stock_critique"] == 0
    assert features["high_priority_workorders"] == 1
    assert features["recent_notifications"] == 1
