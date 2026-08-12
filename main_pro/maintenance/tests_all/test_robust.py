import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention, Signalement
)

@pytest.mark.django_db
def test_workorder_sans_technicien():
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO sans tech", cree_par=expert, machine=machine, expert=expert)

    # Aucun technicien assigné → WorkOrder doit rester en attente
    assert wo.techniciens.count() == 0
    assert wo.etat == "en_attente"


@pytest.mark.django_db
def test_intervention_sans_dates():
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    cat = Categorie.objects.create(nom="electrique")
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO sans dates", cree_par=expert, machine=machine, expert=expert)
    wo.techniciens.add(tech)

    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech)

    # Pas de date_debut ni date_fin → état doit rester en attente
    assert interv.etat == "en_attente"
    assert wo.etat == "en_attente"


@pytest.mark.django_db
def test_validation_sans_expert():
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    cat = Categorie.objects.create(nom="electrique")
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO sans validation expert", cree_par=expert, machine=machine, expert=expert)
    wo.techniciens.add(tech)

    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech)
    interv.date_debut = timezone.now()
    interv.date_fin = timezone.now()
    # ⚠️ Ne pas définir date_validation sans valide_par
    interv.save()

    # Intervention reste "termine" → WorkOrder pas clos
    assert interv.etat == "termine"
    wo.refresh_from_db()
    assert wo.etat != "clos"


@pytest.mark.django_db
def test_signalement_avec_machine_obligatoire():
    operateur = Utilisateur.objects.create(username="op1", role="operateur")
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")
    sig = Signalement.objects.create(
        description="Signalement avec machine obligatoire",
        source="manuel",
        cree_par=operateur,
        machine=machine  # ✅ machine obligatoire
    )

    assert sig.machine == machine
    machine.refresh_from_db()
    assert machine.etat == "PANNE"
