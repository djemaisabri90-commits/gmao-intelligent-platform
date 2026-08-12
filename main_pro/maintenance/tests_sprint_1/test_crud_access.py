from rest_framework import status
from rest_framework.test import APITestCase
from maintenance.models import Categorie, Utilisateur, Machine


class TestPermissions(APITestCase):

    def setUp(self):

        # Nettoyage
        Categorie.objects.all().delete()
        Utilisateur.objects.all().delete()
        Machine.objects.all().delete()

        self.url_users = "/api/maintenance/utilisateurs/"
        self.url_machines = "/api/maintenance/machines/"

        # Création admin
        self.admin = Utilisateur.objects.create_user(
            username="admin_test",
            password="admin1234",
            role="admin"
        )

        # Création technicien
        self.technicien = Utilisateur.objects.create_user(
            username="tech_test",
            password="tech1234",
            role="technicien"
        )

        # Création machine
        self.machine = Machine.objects.create(
            nom="Machine_Test"
        )


    # ======================
    # Création technicien
    # ======================

    def test_admin_ajoute_technicien_avec_categorie(self):

        print("\n=== TEST : Admin ajoute technicien avec catégorie ===")

        self.client.force_authenticate(
            user=self.admin
        )

        categorie = Categorie.objects.create(
            nom="mecanique",
            description="Maintenance mecanique"
        )

        data = {
            "username": "tech_api",
            "password": "test1234",
            "role": "technicien",
            "categorie": categorie.pk
        }

        response = self.client.post(
            self.url_users,
            data,
            format="json"
        )

        print("Code retour :", response.status_code)
        print("Réponse :", response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Échec : admin devrait pouvoir créer un technicien."
        )

        print("✓ Succès : technicien créé")


    # ======================
    # CRUD Utilisateur
    # ======================

    def test_non_authentifie_ne_peut_pas_creer_utilisateur(self):

        print("\n=== TEST : utilisateur non authentifié ajoute utilisateur ===")

        response = self.client.post(
            self.url_users,
            {
                "username": "test",
                "password": "1234"
            }
        )

        print("Code retour :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Échec : utilisateur non connecté autorisé."
        )

        print("✓ Accès refusé (401)")


    def test_technicien_ne_peut_pas_supprimer_utilisateur(self):

        print("\n=== TEST : technicien supprime utilisateur ===")

        self.client.force_authenticate(
            user=self.technicien
        )

        response = self.client.delete(
            f"{self.url_users}{self.admin.id}/"
        )

        print("Code retour :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Échec : technicien autorisé à supprimer utilisateur."
        )

        print("✓ Suppression refusée (403)")


    # ======================
    # CRUD Machine
    # ======================

    def test_non_authentifie_ne_peut_pas_ajouter_machine(self):

        print("\n=== TEST : non authentifié ajoute machine ===")

        response = self.client.post(
            self.url_machines,
            {
                "nom": "Machine X"
            }
        )

        print("Code retour :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Échec : ajout machine sans authentification autorisé."
        )

        print("✓ Accès refusé (401)")


    def test_technicien_ne_peut_pas_supprimer_machine(self):

        print("\n=== TEST : technicien supprime machine ===")

        self.client.force_authenticate(
            user=self.technicien
        )

        response = self.client.delete(
            f"{self.url_machines}{self.machine.id}/"
        )

        print("Code retour :", response.status_code)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Échec : technicien autorisé à supprimer machine."
        )

        print("✓ Suppression machine refusée (403)")