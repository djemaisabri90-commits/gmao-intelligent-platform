import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention, Piece, PieceUtilisee
)

@pytest.mark.django_db
def test_charge_simultanee_multi_techniciens():
    # 1. Création de catégorie et rôles
    cat = Categorie.objects.create(nom="mécanique")
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    tech1 = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    tech2 = Utilisateur.objects.create(username="tech2", role="technicien", categorie=cat)
    tech3 = Utilisateur.objects.create(username="tech3", role="technicien", categorie=cat)

    # 2. Création machine et WorkOrder
    machine = Machine.objects.create(nom="Machine Charge Simultanée", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO Charge Simultanée", cree_par=expert, expert=expert, machine=machine)
    wo.techniciens.add(tech1, tech2, tech3)

    # 3. Création d’une pièce avec stock initial
    piece = Piece.objects.create(nom="Roulement", reference="R002", stock_disponible=30, fournisseur="SKF")

    # 4. Trois interventions simultanées (chaque technicien consomme 10 pièces)
    interventions = []
    for tech in [tech1, tech2, tech3]:
        interv = Intervention.objects.create(workorder=wo)
        interv.techniciens.add(tech)
        interv.date_debut = timezone.now()
        interv.date_fin = timezone.now()
        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()

        PieceUtilisee.objects.create(intervention=interv, piece=piece, quantite=10)
        interventions.append(interv)

    # 5. Vérifier que toutes les interventions sont validées
    assert all(interv.etat == "valide" for interv in interventions)

    # 6. Vérifier que le WorkOrder est clos automatiquement
    wo.refresh_from_db()
    assert wo.etat == "clos"

    # 7. Vérifier que la machine est revenue en SERVICE
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"

    # 8. Vérifier que le stock est décrémenté correctement (30 - 3*10 = 0)
    piece.refresh_from_db()
    assert piece.stock_disponible == 0

    # 9. Vérifier que le stock n’est jamais négatif
    assert piece.stock_disponible >= 0
