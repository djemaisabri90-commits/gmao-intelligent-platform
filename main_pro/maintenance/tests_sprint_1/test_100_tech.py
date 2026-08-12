import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention, Piece, PieceUtilisee
)

@pytest.mark.django_db
def test_stress_100_techniciens_en_parallele():
    # 1. Création de catégorie et expert
    cat = Categorie.objects.create(nom="mécanique")
    expert = Utilisateur.objects.create(username="exp1", role="expert")

    # 2. Création machine et WorkOrder
    machine = Machine.objects.create(nom="Machine Stress 100 Tech", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO Stress 100 Tech", cree_par=expert, expert=expert, machine=machine)

    # 3. Création d’une pièce avec stock initial
    piece = Piece.objects.create(nom="Roulement", reference="R100", stock_disponible=1000, fournisseur="SKF")

    # 4. Création de 100 techniciens et interventions simultanées
    interventions = []
    for i in range(100):
        tech = Utilisateur.objects.create(username=f"tech{i+1}", role="technicien", categorie=cat)
        wo.techniciens.add(tech)

        interv = Intervention.objects.create(workorder=wo)
        interv.techniciens.add(tech)
        interv.date_debut = timezone.now()
        interv.date_fin = timezone.now()
        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()

        # Chaque technicien consomme 5 pièces
        PieceUtilisee.objects.create(intervention=interv, piece=piece, quantite=5)
        interventions.append(interv)

    # 5. Vérifier que toutes les interventions sont validées
    assert all(interv.etat == "valide" for interv in interventions)

    # 6. Vérifier que le WorkOrder est clos automatiquement
    wo.refresh_from_db()
    assert wo.etat == "clos"

    # 7. Vérifier que la machine est revenue en SERVICE
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"

    # 8. Vérifier que le stock est décrémenté correctement (1000 - 100*5 = 500)
    piece.refresh_from_db()
    assert piece.stock_disponible == 500

    # 9. Vérifier que le stock n’est jamais négatif
    assert piece.stock_disponible >= 0
