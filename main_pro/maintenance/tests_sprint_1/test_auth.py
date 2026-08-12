from rest_framework.test import APITestCase
from rest_framework import status
from maintenance.models import Utilisateur


class TestJWTAuthentication(APITestCase):

    def setUp(self):

        self.url = "/api/maintenance/auth/login/"

        self.user = Utilisateur.objects.create_user(
            username="admin_test",
            password="admin1234",
            role="admin"
        )


    # ======================
    # Connexion réussie
    # ======================

    def test_login_reussi(self):

        print("\n=== TEST : connexion valide ===")

        data = {
            "username": "admin_test",
            "password": "admin1234"
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )

        print("Code :", response.status_code)
        print("Réponse :", response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Échec : connexion valide refusée."
        )

        self.assertIn(
            "access",
            response.data,
            "Échec : token access absent."
        )

        self.assertIn(
            "refresh",
            response.data,
            "Échec : token refresh absent."
        )

        print("✓ JWT généré correctement")


    # ======================
    # Mot de passe incorrect
    # ======================

    def test_login_mot_de_passe_incorrect(self):

        print("\n=== TEST : mot de passe incorrect ===")

        response = self.client.post(
            self.url,
            {
                "username": "admin_test",
                "password": "wrong"
            }
        )

        print("Code :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Échec : mot de passe invalide accepté."
        )

        print("✓ Authentification refusée")


    # ======================
    # Utilisateur inexistant
    # ======================

    def test_login_utilisateur_inexistant(self):

        print("\n=== TEST : utilisateur inexistant ===")

        response = self.client.post(
            self.url,
            {
                "username": "fake",
                "password": "123"
            }
        )

        print("Code :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Échec : utilisateur inexistant accepté."
        )

        print("✓ Refus correct")


    # ======================
    # Champs vides
    # ======================

    def test_login_champs_vides(self):

        print("\n=== TEST : champs vides ===")

        response = self.client.post(
            self.url,
            {}
        )

        print("Code :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Échec : authentification sans données autorisée."
        )

        print("✓ Validation correcte")


    # ======================
    # Vérifier rôle retourné
    # ======================

    def test_retour_role(self):

        print("\n=== TEST : retour rôle utilisateur ===")

        response = self.client.post(
            self.url,
            {
                "username": "admin_test",
                "password": "admin1234"
            }
        )

        self.assertEqual(
            response.data["user"]["role"],
            "admin",
            "Échec : rôle incorrect."
        )

        print("✓ Rôle retourné correctement")


    # ======================
    # Changement mot de passe
    # ======================

    def test_must_change_password(self):

        print("\n=== TEST : obligation changement mot de passe ===")

        self.user.must_change_password = True
        self.user.save()

        response = self.client.post(
            self.url,
            {
                "username": "admin_test",
                "password": "admin1234"
            }
        )

        self.assertTrue(
            response.data["user"]["must_change_password"],
            "Échec : indicateur changement mot de passe absent."
        )

        print("✓ Flag must_change_password retourné")