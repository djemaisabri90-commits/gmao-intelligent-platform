# maintenance/tests/test_user_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from maintenance.models import Categorie, Utilisateur

class UtilisateurAPITest(APITestCase):
    def setUp(self):
        # Nettoyer la base pour éviter les collisions
        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()

        self.url = "/api/maintenance/utilisateurs/"
    
    # tester ajout technicien avec categorie par admin
    def test_admin_ajoute_technicien_avec_categorie(self):
        print("Début du test : création d'un technicien par administrateur")
        # Création administrateur
        admin = Utilisateur.objects.create_user(
        username="admin_test",
        password="admin1234",
        role="admin")
        self.client.force_authenticate(user=admin)
        # Création catégorie
        categorie = Categorie.objects.create(nom="mecanique", description="Maintenance mecanique")
        data = {
        "username": "tech_api",
        "role": "technicien",
        "password": "test1234",
        "categorie": categorie.pk
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED,
        "Échec : l'administrateur devrait pouvoir créer un technicien avec une catégorie valide.")
        self.assertEqual(
        response.data["role"], "technicien",
        "Échec : le rôle attribué devrait être 'technicien'.")

        self.assertEqual(response.data["categorie"], categorie.pk,
        "Échec : la catégorie du technicien créée ne correspond pas à celle fournie.")

        self.assertEqual(response.data["username"], "tech_api",
        "Échec : le nom d'utilisateur créé est incorrect.")
        print("=== TEST : Création d'un technicien avec catégorie par administrateur ===")