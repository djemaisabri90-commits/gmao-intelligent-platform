import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    """Fixture pour injecter le client de test DRF."""
    return APIClient()

@pytest.fixture
def create_initial_user(db):
    """Fixture pour créer un utilisateur de test."""
    return User.objects.create_user(
        username="tech_ouvrier_20",
        password="MotDePasseTemporaire123!",
        role="technicien",
        activation_token="token-unique-gmao-123" # Évite d'attendre le signal en test
    )


@pytest.mark.django_db
def test_change_password_success_with_valid_token(api_client, create_initial_user):
    """
    CAS 1 : Succès de l'auto-activation.
    L'utilisateur est connecté, fournit le bon jeton et un mot de passe fort.
    """
    user = create_initial_user
    
    # 1. Authentification de la requête (Simule l'Axios Interceptor)
    api_client.force_authenticate(user=user)
    
    # 2. 🎯 CORRECTION : Utilisation du nom de route DRF standard au pluriel
    url = reverse("maintenance:utilisateur-change-password", kwargs={"pk": user.pk})
    
    # 3. Données du formulaire (ResetPassword.tsx)
    payload = {
        "activation_token": user.activation_token,
        "password": "NouveauSuperMotDePasse@2026"  # Passe la validation de force
    }
    
    response = api_client.post(url, payload, format="json")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "Mot de passe changé avec succès"
    
    user.refresh_from_db()
    assert user.must_change_password is False


@pytest.mark.django_db
def test_change_password_fails_with_invalid_token(api_client, create_initial_user):
    """
    CAS 2 : Blocage de sécurité.
    L'utilisateur fournit un mauvais token d'activation.
    """
    user = create_initial_user
    api_client.force_authenticate(user=user)
    
    # 🎯 CORRECTION : Même nom de route corrigé ici
    url = reverse("maintenance:utilisateur-change-password", kwargs={"pk": user.pk})
    
    payload = {
        "activation_token": "MAUVAIS-TOKEN-456",
        "password": "NouveauSuperMotDePasse@2026"
    }
    
    response = api_client.post(url, payload, format="json")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Le code d'activation fourni est incorrect."
    
    user.refresh_from_db()
    assert user.must_change_password is True
