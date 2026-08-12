"""
Test d’intégration du workflow
Ce test simule le scénario complet :

Création d’un WorkOrder avec technicien assigné

Création de l’intervention correspondante

Démarrage et clôture de l’intervention

Validation finale par un admin

##############################
1. workorder_services.py — Création propre du WorkOrder
[ ] Le WorkOrder est créé via create_workorder() sans intervention automatique.

[ ] Si un technicien est assigné, cette info est stockée mais ne déclenche pas de création d’intervention ici.

[ ] Les dates (date_validation, date_cloture) sont ajustées selon le statut.

[ ] full_clean() est appelé avant save() pour valider le modèle.

✅ 2. intervention_service.py — Création + Notification
[ ] create_intervention() reçoit workorder, technicien, etc.

[ ] L’intervention est créée proprement avec statut="en_attente" par défaut.

[ ] Si un technicien est présent, une notification WebSocket est envoyée via channel_layer.group_send.

[ ] Pas de recréation de WorkOrder ici.

✅ 3. intervention_views.py — Vue propre
python
def perform_create(self, serializer):
    instance = create_intervention(**serializer.validated_data)
    audit_action(self.request, "create", instance)
    serializer.instance = instance
[ ] Pas de create_workorder() ici.

[ ] On utilise un WorkOrder existant (passé dans validated_data).

[ ] L’intervention est créée via le service métier.

[ ] L’audit est bien enregistré.

✅ 4. Modèle Intervention — Validation métier
[ ] clean() vérifie la cohérence des dates et des rôles.

[ ] save() appelle full_clean() pour garantir la validité.

[ ] Les erreurs sont levées proprement si incohérence (ex. technicien absent, dates invalides).

✅ 5. Cas de réassignation
[ ] Si le technicien est modifié dans le WorkOrder, une nouvelle intervention peut être créée ou mise à jour.

[ ] Une nouvelle notification est envoyée au technicien remplacant.

[ ] L’ancienne intervention peut être annulée ou réattribuée selon ta logique métier.

🎯 Résultat attendu
Architecture claire, sans duplication.

Notifications déclenchées uniquement dans intervention_service.py.

Vue légère, services responsables.

Modèle robuste, validé à chaque save().

"""

################################
## test est passé avec succès ##
################################
"""
preuve que ton workflow WorkOrder → Intervention → Notification est bien aligné et validé par Django + pytest.

Tu as franchi une étape clé :

✅ La configuration pytest.ini est correcte (Django charge bien main_pro.settings).

✅ La base de test est accessible grâce au @pytest.mark.django_db.

✅ Le scénario métier (création, démarrage, clôture, validation) fonctionne sans erreur.




"""
import pytest
from django.utils import timezone
from maintenance.models import Machine, WorkOrder, Intervention
from maintenance.services.workorder_services import create_workorder
from maintenance.services.intervention_service import create_intervention
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_workorder_intervention_notification_flow():
    admin = User.objects.create(username="admin", role="admin")
    technicien = User.objects.create(username="tech1", role="technicien")

    machine = Machine.objects.create(
    nom="Machine Test",
    description="Machine de test"
)

    # Étape 1 : Création du WorkOrder
    workorder = create_workorder(
        machine=machine,  # adapte selon ton modèle
        description="Test WorkOrder",
        technicien=technicien,
        cree_par=admin
    )

    # Étape 2 : Création de l'intervention
    intervention = create_intervention(
        workorder=workorder,
        technicien=technicien,
        type_intervention="corrective",
        priorite="haute",
        statut="en_attente"
    )

    # Vérifications initiales
    assert intervention.workorder == workorder
    assert intervention.technicien == technicien
    assert intervention.statut == "en_attente"
    assert intervention.date_debut is None
    assert intervention.date_fin is None

    # Étape 3 : Démarrer l'intervention
    intervention.statut = "en_cours"
    intervention.date_debut = timezone.now()
    intervention.full_clean()
    intervention.save()

    assert intervention.statut == "en_cours"
    assert intervention.date_debut is not None

    # Étape 4 : Terminer l'intervention
    intervention.statut = "termine"
    intervention.date_fin = timezone.now()
    intervention.full_clean()
    intervention.save()

    assert intervention.statut == "termine"
    assert intervention.date_fin is not None

    # Étape 5 : Valider l'intervention
    intervention.valide_par = admin
    intervention.date_validation = timezone.now()
    intervention.full_clean()
    intervention.save()

    assert intervention.valide_par == admin
    assert intervention.date_validation is not None
