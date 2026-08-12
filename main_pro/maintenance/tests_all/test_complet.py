import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, Signalement,
    WorkOrder, Intervention, Piece, PieceUtilisee, Notification
)

@pytest.mark.django_db
def test_flux_complet_signalement_workorder_intervention():
    # 1. Création des rôles
    cat = Categorie.objects.create(nom="electrique")
    operateur = Utilisateur.objects.create(username="op1", role="operateur")
    expert = Utilisateur.objects.create(username="exp1", role="expert")
    tech1 = Utilisateur.objects.create(username="tech1", role="technicien", categorie=cat)
    tech2 = Utilisateur.objects.create(username="tech2", role="technicien", categorie=cat)

    # 2. Création d'une machine
    machine = Machine.objects.create(nom="Machine Test", etat="SERVICE")

    # 3. L’opérateur crée un signalement
    sig = Signalement.objects.create(
        machine=machine,
        description="Panne électrique",
        source="manuel",
        cree_par=operateur
    )
    assert sig.statut == "nouveau"
    print('\nNouveau signalement créé')

    # 4. Notification pour l’expert (simulée)
    notif = Notification.objects.create(
        user=expert,
        message=f"Nouveau signalement {sig.id}",
        type=Notification.NotificationType.WORKORDER_CREATED,
        workorder=None
    )
    assert notif.user == expert

    # 5. L’expert crée un WorkOrder lié au signalement
    wo = WorkOrder.objects.create(
        signalement=sig,
        machine=machine,
        categorie=cat,
        description="Réparation électrique",
        cree_par=expert,
        expert=expert
    )
    wo.techniciens.add(tech1, tech2)
    assert wo.techniciens.count() == 2

    # 6. Création d’une intervention
    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech1, tech2)

    # 7. Les techniciens démarrent et terminent l’intervention
    interv.date_debut = timezone.now()
    interv.actions_realisees = "Réparation câblage"
    interv.save()
    assert interv.etat == "en_cours"

    interv.date_fin = timezone.now()
    interv.save()
    assert interv.etat == "termine"

    # 8. Utilisation de pièces
    piece = Piece.objects.create(nom="Câble électrique", reference="CAB123", stock_disponible=10, fournisseur="FournisseurX")
    PieceUtilisee.objects.create(intervention=interv, piece=piece, quantite=2)
    piece.refresh_from_db()
    assert piece.stock_disponible == 8

    # 9. Validation par l’expert
    interv.date_validation = timezone.now()
    interv.valide_par = expert
    interv.is_locked = True
    interv.save()
    assert interv.etat == "valide"

    # 10. Vérifier que le WorkOrder est automatiquement clos
    wo.refresh_from_db()
    assert wo.etat == "clos"
    assert wo.date_cloture is not None

    # 11. Vérifier que la machine est mise à jour
    machine.refresh_from_db()
    assert machine.etat == "SERVICE"

    # 12. Vérifier qu’une notification de clôture est créée
    notif_cloture = Notification.objects.filter(workorder=wo).first()
    assert notif_cloture is not None
    assert "clôturé automatiquement" in notif_cloture.message
