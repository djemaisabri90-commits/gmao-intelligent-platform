import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, WorkOrder, Intervention,
    Piece, PieceUtilisee
)

@pytest.mark.django_db
def test_stock_pieces_multi_interventions():
    # 1. Création des rôles et catégorie
    cat = Categorie.objects.create(nom="electrique")
    tech1 = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    tech2 = Utilisateur.objects.create(username="tech2", role="technicien", categorie=cat)
    expert = Utilisateur.objects.create(username="exp1", role="expert")

    # 2. Création d'une machine
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")

    # 3. Création du WorkOrder
    wo = WorkOrder.objects.create(description="WO Stock Test", cree_par=expert, machine=machine, expert=expert)
    wo.techniciens.add(tech1, tech2)

    # 4. Création d'une pièce
    piece = Piece.objects.create(nom="Câble électrique", reference="CAB123", stock_disponible=10, fournisseur="FournisseurX")

    # 5. Première intervention (tech1 utilise 3 câbles)
    interv1 = Intervention.objects.create(workorder=wo)
    interv1.techniciens.add(tech1)
    interv1.date_debut = timezone.now()
    interv1.date_fin = timezone.now()
    PieceUtilisee.objects.create(intervention=interv1, piece=piece, quantite=3)

    piece.refresh_from_db()
    assert piece.stock_disponible == 7  # 10 - 3

    # 6. Deuxième intervention (tech2 utilise 2 câbles)
    interv2 = Intervention.objects.create(workorder=wo)
    interv2.techniciens.add(tech2)
    interv2.date_debut = timezone.now()
    interv2.date_fin = timezone.now()
    PieceUtilisee.objects.create(intervention=interv2, piece=piece, quantite=2)

    piece.refresh_from_db()
    assert piece.stock_disponible == 5  # 7 - 2

    # 7. Validation des interventions par l’expert
    for interv in [interv1, interv2]:
        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()
        assert interv.etat == "valide"

    # 8. Vérifier que le WorkOrder est clos
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None
