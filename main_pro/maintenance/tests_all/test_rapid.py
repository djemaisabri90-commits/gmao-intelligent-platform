import pytest
from maintenance.models import WorkOrder, Intervention

@pytest.mark.django_db
def test_technicien_sees_intervention(api_client, technicien_user, machine):
    # Créer un WorkOrder avec technicien assigné
    wo = WorkOrder.objects.create(
        machine=machine,
        description="Test WO",
        cree_par=technicien_user
    )
    wo.techniciens.add(technicien_user)

    # Créer une Intervention liée
    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(technicien_user)

    # Authentifier le technicien
    api_client.force_authenticate(user=technicien_user)

    # Appeler l’endpoint
    response = api_client.get("/api/maintenance/interventions/")
    assert response.status_code == 200

    data = response.json()
    ids = [i["id"] for i in data]
    assert interv.id in ids
