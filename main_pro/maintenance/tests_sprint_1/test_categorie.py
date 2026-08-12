# maintenance/tests/test_categorie.py

from rest_framework.test import APITestCase
from rest_framework import status
from maintenance.models import (
    Categorie,
    Utilisateur
)

class UtilisateurAPITest(APITestCase):

    def setUp(self):

        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()

        self.url = ("/api/maintenance/utilisateurs/")

        # créer admin
        self.admin = (Utilisateur.objects.create_user(
                username="admin",
                password="admin123",
                role="admin"
            )
        )

    def test_technicien_sans_categorie(self):
        print("\n=== TEST : "
            "Ajouter technicien sans catégorie ==="
        )

        self.client.force_authenticate(user=self.admin)

        data = {

            "username":
            "tech_api_fail",

            "role":
            "technicien",

            "password":
            "test1234"
        }

        response = self.client.post(self.url, data, format="json")

        print("Code :", response.status_code)

        print("Erreur :", response.data)

        self.assertEqual(response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Le système devrait "
            "refuser la création "
            "d’un technicien "
            "sans catégorie."
        )

        self.assertIn("categorie", response.data)

        self.assertEqual(response.data["categorie"][0],
            "Un technicien doit "
            "avoir une catégorie."
        )

        print("✓ Validation " "catégorie correcte")

            
