# maintenance/tests/test_crud_utilisateur.py

from rest_framework.test import APITestCase
from rest_framework import status
from maintenance.models import Utilisateur


class TestCRUDUtilisateur(APITestCase):

    def setUp(self):

        self.url = "/api/maintenance/utilisateurs/"

        self.admin = (
            Utilisateur.objects
            .create_user(

                username="admin",

                password="admin123",

                role="admin"
            )
        )

        self.client.force_authenticate(
            user=self.admin
        )


    # ====================
    # CREATE
    # ====================

    def test_create_utilisateur(self):

        print(
            "\n=== TEST : création utilisateur ==="
        )

        data = {

            "username":
            "user_test",

            "password":
            "test1234",

            "role":
            "admin"
        }

        response = self.client.post(
            self.url,
            data,
            format="json"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        print(
            "✓ Utilisateur créé"
        )


    # ====================
    # READ
    # ====================
    def test_read_utilisateurs(self):
        print("\n=== TEST : liste utilisateurs ===")
        response = (self.client.get(self.url))
        self.assertEqual(response.status_code,status.HTTP_200_OK
        )
        print("✓ Lecture réussie")
    # ====================
    # UPDATE
    # ====================
    def test_update_username(self):
        user = (Utilisateur.objects
            .create_user(username="old",
                password="123",
                role="admin"))
        response = (self.client.patch(f"{self.url}{user.id}/",
                {"username": "new_name"}, format="json"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, "new_name")
        print("✓ Username modifié")
    # ====================
    # DELETE
    # ====================
    def test_delete_utilisateur(self):
        user = (
            Utilisateur.objects
            .create_user(

                username="delete",

                password="123",

                role="admin"
            )
        )


        response = (

            self.client.delete(

                f"{self.url}{user.id}/"
            )
        )


        self.assertEqual(

            response.status_code,

            status.HTTP_204_NO_CONTENT
        )


        print(
            "✓ Utilisateur supprimé"
        )


    # ====================
    # SECURITE
    # ====================

    def test_non_authentifie_refuse(self):

        self.client.force_authenticate(
            user=None
        )


        response = (
            self.client.get(
                self.url
            )
        )


        self.assertEqual(

            response.status_code,

            status.HTTP_401_UNAUTHORIZED
        )
        print("✓ Accès refusé")