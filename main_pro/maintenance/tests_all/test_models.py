import pytest
from maintenance.models import Utilisateur, Categorie, WorkOrder, Intervention, Machine
from django.utils import timezone
@pytest.mark.django_db
def test_utilisateur_categorie_relation():
    # Création d'une catégorie réelle
    cat = Categorie.objects.create(nom="electrique")
    user = Utilisateur.objects.create(username="sabri", role="technicien", categorie=cat)
    assert user.categorie.nom == "electrique"
"""
@pytest.mark.django_db
def test_workorder_cloture_apres_validation():
    user2 = Utilisateur.objects.create(username="sabri", role="admin")
    M = Machine.objects.create(id=1, nom="Test", etat="SERVICE")
    wo = WorkOrder.objects.create(id=1, description="Test", cree_par=user2, machine=M)
    cat = Categorie.objects.create(nom="electrique")
    interv = Intervention.objects.create(id=1, workorder=wo, valide_par=user2)
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    interv.techniciens.add(tech)  # possible car interv est déjà sauvegardé

    interv.date_debut = timezone.now()
    interv.save()
    assert interv.etat == "en_cours"

    interv.date_fin = timezone.now()
    interv.save()
    assert interv.etat == "termine"

    interv.date_validation = timezone.now()
    interv.save()
    assert interv.etat == "valide"
    

    
    
    
    
    
    
    #interv1 = Intervention.objects.create(workorder=wo, etat="en_attente")
    #interv2 = Intervention.objects.create(workorder=wo, etat="en_attente")

    # Toutes les interventions passent en valide
    #interv1.etat = "valide"; interv1.save()
    #interv2.etat = "valide"; interv2.save()

    # Rafraîchir l'objet WorkOrder
    wo.refresh_from_db()
    assert wo.etat == "clos"
"""
