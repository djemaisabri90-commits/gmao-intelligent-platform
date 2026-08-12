import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, Signalement,
    WorkOrder, Intervention
)

@pytest.mark.django_db
def test_workflow_machine_etat():
    # 1. Création des rôles et catégorie
    cat = Categorie.objects.create(nom="electrique")
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    operateur = Utilisateur.objects.create(username="op1", role="operateur")

    # 2. Création d'une machine
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")

    # 3. Signalement créé par l’opérateur → machine en PANNE
    sig = Signalement.objects.create(
        machine=machine,
        description="Panne électrique",
        source="manuel",
        cree_par=operateur
    )
    machine.refresh_from_db()
    assert machine.etat == "PANNE"

    # 4. L’expert crée un WorkOrder
    wo = WorkOrder.objects.create(signalement=sig, machine=machine, categorie=cat, description="Réparation", cree_par=expert, expert=expert)
    wo.techniciens.add(tech)

    # 5. Intervention démarrée → machine en MAINTENANCE
    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech)
    interv.date_debut = timezone.now()
    interv.save()
    machine.refresh_from_db()
    assert machine.etat == "MAINTENANCE"

    # 6. Intervention terminée mais pas validée → machine reste en MAINTENANCE
    interv.date_fin = timezone.now()
    interv.save()
    machine.refresh_from_db()
    assert machine.etat == "MAINTENANCE"

    # 7. Intervention validée par l’expert → machine revient en SERVICE
    interv.date_validation = timezone.now()
    interv.valide_par = expert
    interv.is_locked = True
    interv.save()
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"

    # 8. Vérifier que le WorkOrder est clos
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None
