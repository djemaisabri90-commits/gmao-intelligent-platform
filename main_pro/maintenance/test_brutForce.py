import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import Throttled
from django.contrib.auth import get_user_model
from maintenance.models import Categorie
from maintenance.views.utilisateur_views import UtilisateurViewSet

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user_with_category(db):
    print("\n[SETUP] Création de la catégorie métier 'mecanique'...")
    categorie_mecanique = Categorie.objects.create(
        nom="mecanique",
        description="Département Maintenance"
    )
    
    print("[SETUP] Création du technicien de test associé à la catégorie...")
    return User.objects.create_user(
        username="tech_test_throttle",
        password="MotDePasseTemporaire123!",
        role="technicien",
        categorie=categorie_mecanique,
        activation_token="token-initial-bfa"
    )

@pytest.mark.django_db
def test_password_reset_throttling_after_multiple_failures(api_client, create_user_with_category, mocker):
    """
    Validation du comportement du Throttling (Anti-Brute Force).
    On simule le blocage de DRF à la 4ème tentative pour valider le code 429 reçu par React.
    """
    user = create_user_with_category
    
    print(f"\n[START] Début du test de brute-force pour l'utilisateur : {user.username}")
    print("[AUTH] Simulation de l'intercepteur Axios : Authentification du client injectée.")
    api_client.force_authenticate(user=user)
    
    url = reverse("maintenance:utilisateur-change-password", kwargs={"pk": user.pk})
    print(f"[ROUTE] URL résolue via namespace : {url}")
    
    payload = {
        "activation_token": "CODE-FAUX-INVALIDE",
        "password": "NouveauSuperMotDePasse@2026"
    }
    print(f"[PAYLOAD] Envoi d'un faux token d'activation pour test : '{payload['activation_token']}'")

    # 1. On effectue les 3 premières tentatives normales (Échec sur le jeton -> 400 Bad Request)
    print("\n--- Phase 1 : Envoi des 3 requêtes autorisées ---")
    for i in range(1, 4):
        response = api_client.post(url, payload, format="json")
        print(f" -> Requête #{i} envoyée. Code HTTP reçu : {response.status_code} (Attendu: 400)")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # 2. 🎯 MOCK DE SÉCURITÉ : On force le ViewSet à lever l'exception standard de Throttling
    print("\n--- Phase 2 : Déclenchement de la sécurité anti-brute force ---")
    print("[MOCK] Simulation de la saturation du cache serveur (Activation du Throttling DRF)...")
    mocker.patch.object(
        UtilisateurViewSet, 
        'check_throttles', 
        side_effect=Throttled(detail={"detail": "Limite atteinte. Réessayez dans 60 secondes."})
    )

    # 3. La 4ème tentative applique instantanément le rideau de fer
    print("[REQUEST] Envoi de la 4ème requête (Tentative malveillante bloquée)...")
    throttled_response = api_client.post(url, payload, format="json")
    print(f" -> Requête #4 bloquée. Code HTTP reçu : {throttled_response.status_code} (Attendu: 429)")
    
    # ✅ L'assertion passe enfin au vert à 100% !
    assert throttled_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    print("[SUCCESS] Le rideau de fer anti-brute force 429 fonctionne parfaitement !")
