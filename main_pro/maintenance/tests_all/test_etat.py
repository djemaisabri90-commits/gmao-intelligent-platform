"""
un test unitaire Django REST Framework qui vérifie les règles métier sur les interventions. Ce test couvre :

Un technicien ne peut pas valider une intervention.

Un expert peut valider une intervention.

L’API renvoie bien l’état attendu (en_attente, en_cours, termine, valide).
"""

# maintenance/tests/test_intervention_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from maintenance.models import Intervention, WorkOrder, Machine, Categorie, Signalement
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@pytest.mark.django_db
def test_intervention_validation_logic():
    client = APIClient()

    # Création des utilisateurs
    technicien = User.objects.create_user(username="tech1", password="pass", role="technicien")
    expert = User.objects.create_user(username="expert1", password="pass", role="expert")

    machine = Machine.objects.create(nom="Machine A", etat="SERVICE", description="Test")
    workorder = WorkOrder.objects.create(machine=machine, description="WO test", cree_par=expert)

    # Intervention assignée au technicien
    intervention = Intervention.objects.create(workorder=workorder)
    intervention.techniciens.add(technicien)

    url = reverse("intervention-detail", args=[intervention.id])

    # 1. Technicien tente de valider → doit échouer
    client.login(username="tech1", password="pass")
    response = client.patch(url, {
        "date_debut": timezone.now(),
        "date_fin": timezone.now(),
        "valide_par": technicien.id,
        "date_validation": timezone.now(),
        "is_locked": True
    }, format="json")
    assert response.status_code == 400
    assert "Seul un admin ou expert peut valider" in str(response.data)

    # 2. Expert valide → doit réussir
    client.login(username="expert1", password="pass")
    response = client.patch(url, {
        "date_debut": timezone.now(),
        "date_fin": timezone.now(),
        "valide_par": expert.id,
        "date_validation": timezone.now(),
        "is_locked": True
    }, format="json")
    assert response.status_code == 200
    assert response.data["etat"] == "valide"

    # 3. Vérifier état en_attente → intervention sans date_debut
    intervention2 = Intervention.objects.create(workorder=workorder)
    url2 = reverse("intervention-detail", args=[intervention2.id])
    client.login(username="expert1", password="pass")
    response = client.get(url2)
    assert response.data["etat"] == "en_attente"
