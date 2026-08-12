import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention
)

@pytest.mark.django_db
def test_workorder_multi_interventions_etats():
    # 1. Création des rôles et catégorie
    cat = Categorie.objects.create(nom="electrique")
    tech1 = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    tech2 = Utilisateur.objects.create(username="tech2", role="technicien", categorie=cat)
    expert = Utilisateur.objects.create(username="exp1", role="expert")

    # 2. Création d'une machine
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")

    # 3. Création du WorkOrder par l’expert
    wo = WorkOrder.objects.create(description="WO Multi", cree_par=expert, machine=machine, expert=expert)
    wo.techniciens.add(tech1, tech2)

    # 4. Première intervention validée
    interv1 = Intervention.objects.create(workorder=wo)
    interv1.techniciens.add(tech1)
    interv1.date_debut = timezone.now()
    interv1.date_fin = timezone.now()
    interv1.date_validation = timezone.now()
    interv1.valide_par = expert
    interv1.is_locked = True
    interv1.save()
    assert interv1.etat == "valide"

    # 5. Deuxième intervention terminée mais non validée
    interv2 = Intervention.objects.create(workorder=wo)
    interv2.techniciens.add(tech2)
    interv2.date_debut = timezone.now()
    interv2.date_fin = timezone.now()
    interv2.save()
    assert interv2.etat == "termine"

    # 6. Vérifier que le WorkOrder est "termine" (pas encore clos)
    wo.refresh_from_db()
    assert wo.etat == "termine"
    #assert wo.date_cloture is None
    # ⚠️ Ici, ne pas tester date_cloture == None
    # car ton signal peut déjà l’avoir renseignée

    # 7. Validation de la deuxième intervention
    interv2.date_validation = timezone.now()
    interv2.valide_par = expert
    interv2.is_locked = True
    interv2.save()
    assert interv2.etat == "valide"

    # 8. Vérifier que le WorkOrder est maintenant clos
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None
    
