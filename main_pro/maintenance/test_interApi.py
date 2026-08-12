from rest_framework.test import APITestCase
from django.utils import timezone

from maintenance.models import (
    Categorie,
    Intervention,
    Machine,
    Utilisateur,
    WorkOrder
)


class InterventionTest(APITestCase):


    def setUp(self):

        self.tech = Utilisateur.objects.create_user(

            username="tech",

            role="technicien"

        )

        self.admin = Utilisateur.objects.create_user(

            username="admin",

            role="admin"

        )

        # créer catégorie valide
        self.categorie = Categorie.objects.create(

            nom="Mécanique"

            # ajouter autres champs obligatoires
        )


        # créer machine valide
        self.machine = Machine.objects.create(

            nom="Machine test"

            # ajouter autres champs obligatoires
        )

        

        self.workorder = WorkOrder.objects.create(

            machine=self.machine,

            categorie=self.categorie,


            description="WO test",

            cree_par=self.admin,

            type="corrective"  # adapter à vos choix

        )
        self.intervention = Intervention.objects.create(
            workorder=self.workorder,

            type_intervention="corrective",  # adapter

            priorite="haute"
        )    


    def test_start_intervention(self):

        self.client.force_authenticate(
            self.tech
        )

        self.intervention.techniciens.add(
            self.tech
        )

        response = self.client.post(

            f"/api/maintenance/interventions/{self.intervention.id}/start/"

        )

        self.assertEqual(

            response.status_code,

            200

        )


    def test_finish_intervention(self):

        self.intervention.date_debut = timezone.now()

        self.intervention.save()

        self.intervention.techniciens.add(
            self.tech
        )

        self.client.force_authenticate(
            self.tech
        )

        response = self.client.post(

            f"/api/maintenance/interventions/{self.intervention.id}/finish/"

        )

        self.assertEqual(

            response.status_code,

            200

        )


    def test_validate_intervention(self):

        self.intervention.date_debut = timezone.now()
        self.intervention.date_fin = timezone.now()

        self.intervention.save()

        self.client.force_authenticate(

            self.admin

        )

        response = self.client.post(

            f"/api/maintenance/interventions/{self.intervention.id}/validate/"

        )

        self.intervention.refresh_from_db()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(

            self.intervention.is_locked

        )