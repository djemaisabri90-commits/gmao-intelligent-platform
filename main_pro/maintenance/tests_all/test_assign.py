import pytest
from django.utils import timezone
from maintenance.models import Utilisateur, Categorie, WorkOrder, Intervention, Machine, Notification

@pytest.mark.django_db
def test_workorder_cloture_auto_signal():
    # 1. Création d'une catégorie
    cat = Categorie.objects.create(nom="electrique")

    # 2. Création d'un technicien
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)

    # 3. Création d'un admin
    admin = Utilisateur.objects.create(username="admin1", role="admin")

    # 4. Création d'une machine
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")

    # 5. Création du WorkOrder
    wo = WorkOrder.objects.create(description="WO Test", cree_par=admin, machine=machine)
    wo.techniciens.add(tech)

    # 6. Création d'une intervention
    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech)

    # 7. Validation de l'intervention par l'admin
    interv.date_debut = timezone.now()
    interv.date_fin = timezone.now()
    interv.date_validation = timezone.now()
    interv.valide_par = admin
    interv.is_locked = True
    interv.save()

    # 8. Vérifier que le WorkOrder est automatiquement clos
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None

    # 9. Vérifier que la machine est mise à jour
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"  # car toutes les interventions sont validées

    # 10. Vérifier qu'une notification est créée
    notif = Notification.objects.filter(workorder=wo).first()
    assert notif is not None
    assert notif.user == wo.cree_par
    assert "clôturé automatiquement" in notif.message
