# maintenance/tests/test_intervention.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from maintenance.models import WorkOrder, Machine, Intervention
from maintenance.services.intervention_service import (
    create_intervention,
    start_intervention,
    finish_intervention,
    validate_intervention,
    change_intervention_status
)
from maintenance.services.audit_service import audit_action
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class InterventionServiceTest(TestCase):
    def setUp(self):
        # Créer un utilisateur technicien
        self.technicien = User.objects.create_user(
            username='tech1',
            password='test123',
            role='technicien'
        )
        # Créer un expert
        self.expert = User.objects.create_user(
            username='expert1',
            password='test123',
            role='expert'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            password='test123',
            role='admin'
        )
        # Créer une machine
        self.machine = Machine.objects.create(nom='Machine test')
        # Créer un workorder
        self.workorder = WorkOrder.objects.create(
            machine=self.machine,
            description='Test workorder',
            technicien=self.technicien,
            statut='en_attente',
            cree_par=self.admin
        )
        # Créer une intervention
        self.intervention = Intervention.objects.create(
            workorder=self.workorder,
            technicien=self.technicien,
            statut='en_attente'
        )

    def test_create_intervention(self):
        """La création doit mettre statut='en_attente' et date_debut=None"""
        self.assertEqual(self.intervention.statut, 'en_attente')
        self.assertIsNone(self.intervention.date_debut)
        self.assertIsNone(self.intervention.date_fin)

    def test_start_intervention(self):
        """Démarrer une intervention doit passer le statut à 'en_cours' et remplir date_debut"""
        start_intervention(self.intervention, self.technicien)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'en_cours')
        self.assertIsNotNone(self.intervention.date_debut)

    def test_finish_intervention(self):
        """Terminer une intervention doit passer le statut à 'termine' et remplir date_fin"""
        start_intervention(self.intervention, self.technicien)
        finish_intervention(self.intervention, self.technicien)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'termine')
        self.assertIsNotNone(self.intervention.date_fin)
        self.assertGreaterEqual(self.intervention.date_fin, self.intervention.date_debut)

    def test_validate_intervention(self):
        """Valider une intervention doit passer le statut à 'valide' et verrouiller"""
        start_intervention(self.intervention, self.technicien)
        finish_intervention(self.intervention, self.technicien)
        print(self.intervention.statut)
        validate_intervention(self.intervention, self.expert)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'termine')
        self.assertTrue(self.intervention.is_locked)
        self.assertEqual(self.intervention.valide_par, self.expert)
        self.assertIsNotNone(self.intervention.date_validation)

    def test_change_status_via_service(self):
        """Changer le statut via change_intervention_status doit fonctionner"""
        # en_attente -> en_cours
        change_intervention_status(self.intervention, 'en_cours', self.technicien)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'en_cours')
        self.assertIsNotNone(self.intervention.date_debut)

        # en_cours -> termine
        change_intervention_status(self.intervention, 'termine', self.technicien)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'termine')
        self.assertIsNotNone(self.intervention.date_fin)

    def test_suspend_intervention(self):
        """Suspendre une intervention (en_cours -> en_attente) doit effacer date_fin"""
        start_intervention(self.intervention, self.technicien)
        change_intervention_status(self.intervention, 'en_attente', self.technicien)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'en_attente')
        self.assertIsNone(self.intervention.date_fin)

    def test_validation_fails_if_not_terminated(self):
        """La validation doit échouer si l'intervention n'est pas terminée"""
        with self.assertRaises(Exception):
            validate_intervention(self.intervention, self.expert)


class InterventionAPITest(APITestCase):
    def setUp(self):
        self.technicien = User.objects.create_user(
            username='tech_api',
            password='test123',
            role='technicien'
        )
        self.admin = User.objects.create_user(
            username='adm_api',
            password='test123',
            role='admin'
        )
        self.client.force_authenticate(user=self.technicien)
        self.machine = Machine.objects.create(nom='Machine API')
        self.workorder = WorkOrder.objects.create(
            machine=self.machine,
            description='Workorder API',
            technicien=self.technicien,
            cree_par=self.admin
        )
        self.intervention = Intervention.objects.create(
            workorder=self.workorder,
            technicien=self.technicien,
            statut='en_attente'
        )

    def test_start_endpoint(self):
        url = f'/api/maintenance/interventions/{self.intervention.id}/start/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'en_cours')

    def test_finish_endpoint(self):
        self.intervention.statut = 'en_cours'
        self.intervention.save()
        url = f'/api/maintenance/interventions/{self.intervention.id}/finish/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'termine')
        self.assertIsNotNone(self.intervention.date_fin)

    def test_change_statut_endpoint(self):
        self.intervention.statut = 'en_cours'
        self.intervention.save()
        url = f'/api/maintenance/interventions/{self.intervention.id}/change-statut/'
        response = self.client.post(url, {'statut': 'termine'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.statut, 'termine')