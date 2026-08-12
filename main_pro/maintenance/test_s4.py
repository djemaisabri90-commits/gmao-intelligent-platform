import pytest
from django.utils import timezone

from maintenance.models import (
    Utilisateur,
    Categorie,
    Machine,
    WorkOrder,
    Intervention,
    Piece,
    PieceUtilisee
)


@pytest.mark.django_db
def test_stock_pieces_multi_interventions():

    print("\n==============================")
    print(" TEST SPRINT 4 - GESTION DES PIECES ")
    print("==============================\n")

    # -------------------------
    # Création acteurs
    # -------------------------
    cat = Categorie.objects.create(nom="electrique")

    tech1 = Utilisateur.objects.create(
        username="tech1",
        role="technicien",
        categorie=cat
    )

    tech2 = Utilisateur.objects.create(
        username="tech2",
        role="technicien",
        categorie=cat
    )

    expert = Utilisateur.objects.create(
        username="exp1",
        role="expert"
    )

    print("✓ Techniciens et expert créés")

    # -------------------------
    # Machine
    # -------------------------
    machine = Machine.objects.create(
        nom="Machine Test",
        etat="SERVICE"
    )

    print(f"✓ Machine créée : {machine.nom}")

    # -------------------------
    # WorkOrder
    # -------------------------
    wo = WorkOrder.objects.create(
        description="WO Stock Test",
        cree_par=expert,
        machine=machine,
        expert=expert
    )

    wo.techniciens.add(tech1, tech2)

    print(f"✓ WorkOrder créé : #{wo.id}")

    # -------------------------
    # Pièce
    # -------------------------
    piece = Piece.objects.create(
        nom="Câble électrique",
        reference="CAB123",
        stock_disponible=10,
        fournisseur="FournisseurX"
    )

    print(
        f"✓ Pièce créée : {piece.nom} | Stock initial = {piece.stock_disponible}"
    )

    # -------------------------
    # Intervention 1
    # -------------------------
    interv1 = Intervention.objects.create(
        workorder=wo
    )

    interv1.techniciens.add(tech1)

    interv1.date_debut = timezone.now()
    interv1.date_fin = timezone.now()

    PieceUtilisee.objects.create(
        intervention=interv1,
        piece=piece,
        quantite=3
    )

    piece.refresh_from_db()

    print(
        f"✓ Intervention 1 : {tech1.username} consomme 3 pièces"
    )

    print(
        f"✓ Stock restant après intervention 1 : {piece.stock_disponible}"
    )

    assert piece.stock_disponible == 7

    # -------------------------
    # Intervention 2
    # -------------------------
    interv2 = Intervention.objects.create(
        workorder=wo
    )

    interv2.techniciens.add(tech2)

    interv2.date_debut = timezone.now()
    interv2.date_fin = timezone.now()

    PieceUtilisee.objects.create(
        intervention=interv2,
        piece=piece,
        quantite=2
    )

    piece.refresh_from_db()

    print(
        f"✓ Intervention 2 : {tech2.username} consomme 2 pièces"
    )

    print(
        f"✓ Stock restant après intervention 2 : {piece.stock_disponible}"
    )

    assert piece.stock_disponible == 5

    # -------------------------
    # Validation expert
    # -------------------------
    for interv in [interv1, interv2]:

        interv.date_validation = timezone.now()
        interv.valide_par = expert
        interv.is_locked = True
        interv.save()

        print(
            f"✓ Intervention #{interv.id} validée"
        )

        assert interv.etat == "valide"

    # -------------------------
    # Clôture WO
    # -------------------------
    wo.refresh_from_db()

    print(
        f"✓ Etat final WorkOrder : {wo.etat}"
    )

    assert wo.etat == "clos"
    assert wo.date_cloture is not None

    print("\n✓ STOCK FINAL :", piece.stock_disponible)
    print("✓ WORKORDER CLOTURE AUTOMATIQUEMENT")
    print("✓ TEST VALIDE AVEC SUCCES\n")