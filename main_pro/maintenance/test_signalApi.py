from rest_framework.test import APITestCase
from rest_framework import status

from maintenance.models import (
    Utilisateur,
    Machine,
    Signalement,
)


class SignalementAPITest(APITestCase):

    def setUp(self):

        self.user = Utilisateur.objects.create_user(
            username="operateur",
            password="Test123!",
            role="operateur"
        )

        self.machine = Machine.objects.create(
            nom="Machine 1",
            type="Pompe"
        )

        self.client.force_authenticate(
            user=self.user
        )


    def test_create_signalement(self):

        data = {

            "machine": self.machine.id,

            "description":
                "Panne détectée",

            "source":
                "manuel"

        }

        response = self.client.post(
            "/api/maintenance/signalements/",
            data, format="json"
        )
        print("\nERREUR:", response.data)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            Signalement.objects.count(),
            1
        )


    def test_consulter_signalement(self):

        Signalement.objects.create(

            machine=self.machine,

            description="Test",

            cree_par=self.user

        )

        response = self.client.get(
            "/api/maintenance/signalements/"
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_close_signalement(self):

        signalement = Signalement.objects.create(

            machine=self.machine,

            description="Test",

            cree_par=self.user

        )

        response = self.client.post(

            f"/api/maintenance/signalements/{signalement.id}/close/"

        )

        signalement.refresh_from_db()

        self.assertEqual(

            signalement.statut,

            "traite"

        )


    def test_non_authentifie_refuse(self):

        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/maintenance/signalements/"
        )

        self.assertEqual(

            response.status_code,

            status.HTTP_401_UNAUTHORIZED

        )