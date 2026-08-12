from rest_framework.test import APITestCase
from maintenance.models import (
    Utilisateur,
    Machine,
    WorkOrder,
    Intervention,
    Categorie
)


class WorkOrderTest(APITestCase):

    def setUp(self):

        self.admin = Utilisateur.objects.create_user(

            username="admin",

            password="123",

            role="admin"

        )


        self.tech = Utilisateur.objects.create_user(

            username="tech",

            password="123",

            role="technicien"

        )


        self.machine = Machine.objects.create(

            nom="Machine"

        )


        self.categorie = Categorie.objects.create(

            nom="Mécanique"

        )


        self.client.force_authenticate(

            self.admin

        )


    def test_create_workorder(self):

        data = {

            "machine":
                self.machine.id,

            "categorie":
                self.categorie.id,

            "description":
                "Maintenance",

            "techniciens":
                [self.tech.id]

        }

        response = self.client.post(

            "/api/maintenance/workorders/",

            data

        )

        self.assertEqual(

            response.status_code,

            201

        )

    """
    def test_auto_create_intervention(self):

        wo = WorkOrder.objects.create(

            machine=self.machine,

            categorie=self.categorie,
            description="description",

            cree_par=self.admin

        )

        wo.techniciens.add(self.tech)

        self.assertTrue(

            Intervention.objects.exists()

        )
    """
    def test_auto_create_intervention(self):

        response = self.client.post(

        "/api/maintenance/workorders/",

        {

            "machine":
                self.machine.id,

            "categorie":
                self.categorie.id,

            "description":
                "Maintenance",

            "type":
                "corrective",

            "techniciens":
                [self.tech.id]

        },

        format="json"

    )


        self.assertEqual(

            response.status_code,

        201

    )


        self.assertTrue(

        Intervention.objects.exists()

    )