from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import check_password
from maintenance.models import Categorie, Utilisateur

class UtilisateurAPITest(APITestCase):
  
    def setUp(self):
        # Nettoyer la base pour éviter les collisions
        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()

        # Création d'une catégorie valide pour les tests
        self.categorie = Categorie.objects.create(
            nom="mecanique", description="Maintenance mecanique"
        )
        self.url = "/api/maintenance/utilisateurs/"

def test_non_authentifie_ne_peut_pas_modifier_password(self):

    response = self.client.post(f"self.url/change_password_by_username/",

        {

            "username": "admin",
            "password": "hack123"
        }
    )

    self.assertEqual(response.status_code, 401,
        "Échec : accès non autorisé."
    )