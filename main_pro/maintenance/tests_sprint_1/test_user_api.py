# maintenance/tests/test_user_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import check_password
from maintenance.models import Categorie, Utilisateur

class UtilisateurAPITest(APITestCase):
    """
    def setUp(self):
        # Création d'une catégorie valide pour les tests
        self.categorie = Categorie.objects.create(
            nom="mecanique", description="Maintenance mecanique"
        )
        self.url = "/api/maintenance/utilisateurs/"
    """

    def setUp(self):
        # Nettoyer la base pour éviter les collisions
        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()

        # Création d'une catégorie valide pour les tests
        self.categorie = Categorie.objects.create(
            nom="mecanique", description="Maintenance mecanique"
        )
        self.url = "/api/maintenance/utilisateurs/"
    """
    def test_create_technicien_with_category(self):
        data = {
            "username": "tech_api",
            "role": "technicien",
            "categorie": self.categorie.pk,  # ✅ ID valide
            "password": "test1234"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_technicien_without_category(self):
        data = {
            "username": "tech_api_fail",
            "role": "technicien",
            "password": "test1234"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categorie", response.data)

    def test_create_admin_with_category(self):
        data = {
            "username": "admin_api_fail",
            "role": "admin",
            "categorie": self.categorie.id,  # ❌ interdit par ta logique métier
            "password": "test1234"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categorie", response.data)

    def test_create_admin_without_category(self):
        data = {
            "username": "admin_api",
            "role": "admin",
            "password": "test1234"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_password_is_hashed_on_creation(self):
        data = {
            "username": "secure_user",
            "role": "admin",
            "password": "plainpassword123"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Récupérer l'utilisateur créé
        user = Utilisateur.objects.get(username="secure_user")

        # Vérifier que le mot de passe n'est pas stocké en clair
        self.assertNotEqual(user.password, "plainpassword123")

        # Vérifier que le hash correspond bien au mot de passe original
        self.assertTrue(check_password("plainpassword123", user.password))


    def test_update_technicien_category(self):
        # Créer un technicien avec une catégorie
        user = Utilisateur.objects.create_user(
            username="tech_update_unique",
            password="oldpass123",
            role="technicien",
            categorie=self.categorie
        )
        new_categorie = Categorie.objects.create(
            nom="electrique", description="Maintenance électrique"
        )

        url = f"{self.url}{user.id}/"
        data = {
            "role": "technicien",  # ✅ préciser le rôle
            "categorie": new_categorie.pk}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.categorie, new_categorie)

    def test_update_user_password(self):
        user = Utilisateur.objects.create_user(
            username="user_update",
            password="oldpass123",
            role="admin"
        )
        url = f"{self.url}{user.id}/"
        data = {"password": "newsecurepass456"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        # Vérifier que le mot de passe est bien hashé
        self.assertTrue(check_password("newsecurepass456", user.password))
        # Vérifier que must_change_password est activé
        self.assertTrue(user.must_change_password)

    def test_update_user_email_and_phone(self):
        user = Utilisateur.objects.create_user(
            username="user_contact",
            password="pass123",
            role="admin"
        )
        url = f"{self.url}{user.id}/"
        data = {"email": "newmail@example.com", "telephone": "123456789"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "newmail@example.com")
        self.assertEqual(user.telephone, "123456789")
    """
    def test_me_endpoint_returns_authenticated_user(self):
        # Créer un utilisateur
        user = Utilisateur.objects.create_user(
            username="me_user",
            password="pass123",
            role="admin",
            email="me@example.com"
        )

        # Authentifier ce user
        self.client.force_authenticate(user=user)

        # Appeler l’endpoint /me
        url = f"{self.url}me/"
        response = self.client.get(url, format="json")

        # Vérifier la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "me_user")
        self.assertEqual(response.data["email"], "me@example.com")
        self.assertEqual(response.data["role"], "admin")
    
    def test_change_password_self(self):
        # Créer un utilisateur
        user = Utilisateur.objects.create_user(
        username="self_pw_user",
        password="oldpass123",
        role="admin"
        )
        # Authentifier ce user
        self.client.force_authenticate(user=user)

        url = f"{self.url}{user.id}/change_password/"
        data = {"password": "newselfpass456"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        # Vérifier que le mot de passe est bien changé
        self.assertTrue(check_password("newselfpass456", user.password))
        # Vérifier que must_change_password est désactivé
        self.assertFalse(user.must_change_password)


    def test_change_password_by_admin(self):
        # Créer deux utilisateurs : admin et technicien
        admin = Utilisateur.objects.create_user(
        username="admin_pw_user",
        password="adminpass123",
        role="admin"
        )
        tech = Utilisateur.objects.create_user(
            username="tech_pw_user",
            password="oldpass123",
            role="technicien",
            categorie=self.categorie
        )
        # Authentifier l’admin
        self.client.force_authenticate(user=admin)

        url = f"{self.url}{tech.id}/change_password/"
        data = {"password": "newtechpass456"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tech.refresh_from_db()
        # Vérifier que le mot de passe est bien changé
        self.assertTrue(check_password("newtechpass456", tech.password))
        # Vérifier que must_change_password est activé
        self.assertTrue(tech.must_change_password)

    def test_list_utilisateurs(self):
        # Créer deux utilisateurs
        Utilisateur.objects.create_user(
            username="list_user1",
            password="pass123",
            role="admin"
        )
        Utilisateur.objects.create_user(
            username="list_user2",
            password="pass456",
            role="technicien",
            categorie=self.categorie
        )
        # Authentifier un admin
        admin = Utilisateur.objects.create_user(
            username="list_admin",
            password="adminpass",
            role="admin"
        )
        self.client.force_authenticate(user=admin)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifier que les deux utilisateurs apparaissent
        usernames = [u["username"] for u in response.data]
        self.assertIn("list_user1", usernames)
        self.assertIn("list_user2", usernames)

    def test_retrieve_utilisateur(self):
        user = Utilisateur.objects.create_user(
            username="retrieve_user",
            password="pass123",
            role="admin",
            email="retrieve@example.com"
        )

        # Authentifier un admin
        admin = Utilisateur.objects.create_user(
            username="retrieve_admin",
            password="adminpass",
            role="admin"
        )
        self.client.force_authenticate(user=admin)

        url = f"{self.url}{user.id}/"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "retrieve_user")
        self.assertEqual(response.data["email"], "retrieve@example.com")
        self.assertEqual(response.data["role"], "admin")
    
    def test_delete_utilisateur(self):
        user = Utilisateur.objects.create_user(
            username="delete_user",
            password="pass123",
            role="admin"
        )

        # Authentifier un admin
        admin = Utilisateur.objects.create_user(
            username="delete_admin",
            password="adminpass",
            role="admin"
        )
        self.client.force_authenticate(user=admin)

        url = f"{self.url}{user.id}/"
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifier que l'utilisateur n'existe plus
        self.assertFalse(Utilisateur.objects.filter(id=user.id).exists())