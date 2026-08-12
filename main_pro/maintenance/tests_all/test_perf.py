import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention
)

@pytest.mark.django_db
def test_workorder_scalabilite_100_interventions():
    # 1. Création des rôles et catégorie
    cat = Categorie.objects.create(nom="electrique")
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)

    # 2. Création d'une machine
    machine = Machine.objects.create(nom="Machine Stress Test", etat="SERVICE")

    # 3. Création du WorkOrder
    wo = WorkOrder.objects.create(description="WO Scalabilité", cree_par=expert, machine=machine, expert=expert)
    wo.techniciens.add(tech)

    # 4. Création de 100 interventions
    interventions = []
    for i in range(100):
        interv = Intervention.objects.create(workorder=wo)
        interv.techniciens.add(tech)
        interv.date_debut = timezone.now()
        interv.date_fin = timezone.now()
        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()
        interventions.append(interv)

    # 5. Vérifier que toutes les interventions sont validées
    assert all(interv.etat == "valide" for interv in interventions)

    # 6. Vérifier que le WorkOrder est clos automatiquement
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None

    # 7. Vérifier que la machine est revenue en SERVICE
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"
