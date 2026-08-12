import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_export_activation_pdf_success(db):
    print("\nScénario de validation \nde la génération des fiches d'activation au format PDF.")

    print("Vérifie l'accès administratif,\n la conformité des en-têtes et l'intégrité du flux binaire.")
    client = APIClient()
    
    print("\n[SETUP] Début de la préparation du contexte de test...")
    
    # 1. Création de l'admin et de l'utilisateur en attente d'activation
    admin_user = User.objects.create_superuser(
        username="admin_pfe", 
        password="AdminPassWord123!", 
        role="admin"
    )
    print(f" -> Superutilisateur créé avec succès : '{admin_user.username}' (Rôle: {admin_user.role})")
    
    ouvrier = User.objects.create_user(
        username="ouvrier_test", 
        password="PassTemp123!", 
        role="operateur", 
        activation_token="xyz-token-abc"
    )
    print(f" -> Utilisateur en attente d'activation créé : '{ouvrier.username}' (Token: {ouvrier.activation_token})")
    
    print("[AUTH] Simulation de la session d'administration : Injection des privilèges de l'Admin dans le client de test.")
    client.force_authenticate(user=admin_user)
    
    # 2. Appel de l'action de liste (detail=False) avec namespace
    url = reverse("maintenance:utilisateur-export-activation-pdf")
    print(f"[ROUTE] Résolution de l'URL reverse via l'espace de noms : '{url}'")
    
    print("[REQUEST] Envoi de la requête HTTP GET vers l'endpoint d'exportation PDF...")
    response = client.get(url)
    print(f" -> Réponse reçue du serveur HTTP. Code statut : {response.status_code}")
    
    # 3. Assertions : Vérification du flux binaire PDF
    print("\n--- Phase 1 : Validation des en-têtes de la réponse HTTP ---")
    print(f" -> Vérification du code d'état attendu (200 OK)...")
    assert response.status_code == status.HTTP_200_OK
    
    print(f" -> Contrôle du type de contenu (MIME Type attendu: application/pdf) : '{response.headers['Content-Type']}'")
    assert response.headers["Content-Type"] == "application/pdf"
    
    print(f" -> Validation de la disposition du contenu (Doit être un fichier joint/attachment) : '{response.headers['Content-Disposition']}'")
    assert "attachment" in response.headers["Content-Disposition"]

    # 4. Reconstitution du contenu binaire depuis le streaming
    print("\n--- Phase 2 : Analyse et reconstruction du flux binaire (Streaming Content) ---")
    print("[STREAM] Reconstitution et assemblage des paquets d'octets (chunks) en mémoire...")
    pdf_content = b"".join(response.streaming_content)
    print(f" -> Taille totale du fichier généré dynamiquement : {len(pdf_content)} octets.")
    
    # Vérification de la signature magique binaire propre à tous les fichiers PDF valides
    print("[SECURITY] Inspection des premiers octets pour valider la signature magique du format PDF (Doit contenir '%PDF')...")
    assert b"%PDF" in pdf_content
    
    print("[SUCCESS] Le document est un fichier PDF valide et structuré. Fin du scénario avec succès.")
