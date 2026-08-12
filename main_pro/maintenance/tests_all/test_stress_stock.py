import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention, Piece, PieceUtilisee
)

@pytest.mark.django_db
def test_stress_stock_pieces_massif():
    # 1. Création des rôles et catégorie
    cat = Categorie.objects.create(nom="mécanique")
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    tech = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)

    # 2. Création d’une machine et d’un WorkOrder
    machine = Machine.objects.create(nom="Machine Stock Stress", etat="SERVICE")
    wo = WorkOrder.objects.create(description="WO Stock Stress", cree_par=expert, expert=expert, machine=machine)
    wo.techniciens.add(tech)

    # 3. Création d’une pièce avec stock initial
    piece = Piece.objects.create(nom="Roulement", reference="R001", stock_disponible=1000, fournisseur="SKF")

    # 4. Création de 50 interventions qui consomment chacune 10 pièces
    for i in range(50):
        interv = Intervention.objects.create(workorder=wo)
        interv.techniciens.add(tech)
        interv.date_debut = timezone.now()
        interv.date_fin = timezone.now()
        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()

        # Consommation via PieceUtilisee (décrémente automatiquement le stock)
        PieceUtilisee.objects.create(intervention=interv, piece=piece, quantite=10)

    # 5. Vérifier que le stock est décrémenté correctement
    piece.refresh_from_db()
    assert piece.stock_disponible == 500  # 1000 - (50 * 10)

    # 6. Vérifier que le stock n’est jamais négatif
    assert piece.stock_disponible >= 0
