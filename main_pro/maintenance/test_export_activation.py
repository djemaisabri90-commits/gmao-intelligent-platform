import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_export_activation_pdf_success(db):
    print("\n ######Scénario de validation####### \n####de la génération des fiches d'activation au format PDF.####")

    print("Vérifie l'accès administratif.")
    client = APIClient()
    
    admin_user = User.objects.create_superuser(
        username="admin_pfe", 
        password="AdminPassWord123!", 
        role="admin"
    )    
    ouvrier = User.objects.create_user(
        username="ouvrier_test", 
        password="PassTemp123!", 
        role="operateur", 
        activation_token="xyz-token-abc"
    )
    print(f"Utilisateur en attente d'activation créé : '{ouvrier.username}' (Token: {ouvrier.activation_token})")
    
    print("Simulation de la session d'administration :\nInjection des privilèges de l'Admin dans le client de test.")
    client.force_authenticate(user=admin_user)
    
    url = reverse("maintenance:utilisateur-export-activation-pdf")
    
    print("Envoi de la requête :\n HTTP GET vers l'endpoint d'exportation PDF...")
    response = client.get(url)
    print(f"Réponse reçue du serveur HTTP.\nCode statut : {response.status_code}")
    
    # 3. Assertions : Vérification du flux binaire PDF
    print("\n--- Phase 1 : Validation des en-têtes de la réponse HTTP ---")
    print(f" ---Vérification du code d'état attendu (200 OK)...")
    assert response.status_code == status.HTTP_200_OK
    
    print(f"Contrôle du type de contenu : '{response.headers['Content-Type']}'")
    assert response.headers["Content-Type"] == "application/pdf"
    
    print(f" ...Validation de la disposition du contenu\n(Doit être un fichier joint/attachment) :\n '{response.headers['Content-Disposition']}'")
    assert "attachment" in response.headers["Content-Disposition"]

    print("\n--- Phase 2 : Analyse et reconstruction du flux binaire (Streaming Content) ---")
    print("[STREAM] Reconstitution et assemblage des paquets d'octets (chunks) en mémoire...")
    pdf_content = b"".join(response.streaming_content)
    print(f" -> Taille totale du fichier généré dynamiquement : {len(pdf_content)} octets.")
    
    # Vérification de la signature magique binaire propre à tous les fichiers PDF valides
    print("[SECURITY] Inspection des premiers octets pour valider la signature magique du format PDF (Doit contenir '%PDF')...")
    assert b"%PDF" in pdf_content
    
    print("[SUCCESS] Le document est un fichier PDF valide et structuré. Fin du scénario avec succès.")
