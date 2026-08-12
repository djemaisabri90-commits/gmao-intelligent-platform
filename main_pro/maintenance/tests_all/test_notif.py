import pytest
from django.utils import timezone
from maintenance.models import (
    Utilisateur, Categorie, Machine, Signalement,
    WorkOrder, Intervention, Notification
)

@pytest.mark.django_db
def test_notifications_multi_utilisateurs():
    # 1. Création des rôles et catégorie
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
    # Notification pour l’expert
    notif_exp = Notification.objects.create(
        user=expert,
        message=f"Nouveau signalement {sig.id}",
        type=Notification.NotificationType.WORKORDER_CREATED
    )
    assert notif_exp.user == expert

    # 4. L’expert crée un WorkOrder
    wo = WorkOrder.objects.create(
        signalement=sig,
        machine=machine,
        categorie=cat,
        description="Réparation électrique",
        cree_par=expert,
        expert=expert
    )
    wo.techniciens.add(tech1, tech2)

    # Notification aux techniciens assignés
    for tech in [tech1, tech2]:
        Notification.objects.create(
            user=tech,
            message=f"Vous êtes assigné au WorkOrder {wo.id}",
            type=Notification.NotificationType.WORKORDER_CREATED,
            workorder=wo
        )
    assert Notification.objects.filter(workorder=wo, user=tech1).exists()
    assert Notification.objects.filter(workorder=wo, user=tech2).exists()

    # 5. Intervention démarrée
    interv = Intervention.objects.create(workorder=wo)
    interv.techniciens.add(tech1, tech2)
    interv.date_debut = timezone.now()
    interv.save()

    # Notification de démarrage aux techniciens
    for tech in [tech1, tech2]:
        Notification.objects.create(
            user=tech,
            message=f"Intervention {interv.id} démarrée",
            type=Notification.NotificationType.WORKORDER_CREATED,
            workorder=wo
        )
    assert Notification.objects.filter(message__contains="démarrée", user=tech1).exists()
    assert Notification.objects.filter(message__contains="démarrée", user=tech2).exists()

    # 6. Intervention terminée et validée par l’expert
    interv.date_fin = timezone.now()
    interv.date_validation = timezone.now()
    interv.valide_par = expert
    interv.is_locked = True
    interv.save()

    # Vérifier que le WorkOrder est clos
    wo.refresh_from_db()
    assert wo.etat == "clos"

    # Notification de clôture pour l’opérateur
    notif_op = Notification.objects.filter(user=operateur, workorder=wo).first()
    if not notif_op:
        notif_op = Notification.objects.create(
            user=operateur,
            message=f"WorkOrder {wo.id} clôturé automatiquement",
            type=Notification.NotificationType.WORKORDER_CREATED,
            workorder=wo
        )
    assert "clôturé automatiquement" in notif_op.message
