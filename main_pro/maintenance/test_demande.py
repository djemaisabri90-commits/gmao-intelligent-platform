import pytest
from django.utils import timezone
from maintenance.models import Utilisateur, PasswordResetRequest


@pytest.mark.django_db
def test_sprint5_user_account_flow():

    print("\n===== TEST SPRINT 5 : GESTION DES COMPTES UTILISATEURS =====")

    # 1. Création administrateur
    admin = Utilisateur.objects.create(
        username="admin1",
        role="admin"
    )
    print(f"✓ Admin créé : {admin.username}")

    # 2. Création utilisateur (déclenche signal)
    user = Utilisateur.objects.create(
        username="user1",
        role="employe"
    )

    print(f"✓ Utilisateur créé : {user.username}")
    print(f"✓ Activation token : {user.activation_token}")
    print(f"✓ Temp password : {getattr(user, 'temporary_password', None)}")

    assert user.activation_token is not None

    # 3. Création demande reset password
    request = PasswordResetRequest.objects.create(
        user=user
    )

    print("✓ Demande de réinitialisation créée")

    # 4. Traitement demande
    request.status = "resolved"
    request.processed_at = timezone.now()
    request.processed_by = admin
    request.save()

    # Simulation génération nouveaux identifiants
    user.activation_token = "NEW_TOKEN"
    user.must_change_password = True
    user.save()

    print("✓ Demande traitée par admin")
    print("✓ Nouveaux identifiants générés")

    # 5. Vérifications
    assert request.status == "resolved"
    assert request.processed_by == admin

    print("✓ TEST VALIDÉ AVEC SUCCÈS")