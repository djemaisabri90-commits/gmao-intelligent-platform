# tests/test_workorder_intervention_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from maintenance.models import WorkOrder, Intervention, Machine, Signalement
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_technicien_sees_his_workorders_and_interventions():
    client = APIClient()

    # 🔹 Créer un technicien
    technicien = User.objects.create_user(
        username="tech1", password="pass123", role="technicien"
    )
    client.force_authenticate(user=technicien)

    # 🔹 Créer un opérateur (cree_par obligatoire pour Signalement)
    operateur = User.objects.create_user(
        username="op1", password="pass123", role="operateur"
    )

    # 🔹 Créer une machine et un signalement
    machine = Machine.objects.create(nom="Machine A")
    signalement = Signalement.objects.create(
        machine=machine,
        description="Problème test",
        source="operateur",
        cree_par=operateur,   # ✅ obligatoire
    )

    # 🔹 Créer un WorkOrder et lier le technicien
    wo = WorkOrder.objects.create(
        machine=machine,
        signalement=signalement,
        description="WO test",
        type="corrective",
        priorite="high",
        cree_par=operateur,   # ✅ cohérent avec ton modèle
    )
    wo.techniciens.add(technicien)

    # 🔹 Créer une Intervention liée au WorkOrder et au technicien
    intervention = Intervention.objects.create(workorder=wo)
    intervention.techniciens.add(technicien)

    # 🔹 Vérifier que le technicien voit son WorkOrder
    url_wo = reverse("maintenance:workorder-list")
    response_wo = client.get(url_wo)
    assert response_wo.status_code == 200
    assert any(item["id"] == wo.id for item in response_wo.json()["results"])
    
    # 🔹 Vérifier que le technicien voit son Intervention
    url_int = reverse("maintenance:intervention-list")
    response_int = client.get(url_int)
    assert response_int.status_code == 200
    assert any(item["id"] == intervention.id for item in response_int.json())

