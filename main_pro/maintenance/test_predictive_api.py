# predictive/test_predictive_api.py

import pytest
from rest_framework.test import APIClient
from maintenance.models import Utilisateur
from predictive.models import TrainingLog

pytestmark = pytest.mark.django_db


class TestPredictiveDashboard:

    def setup_method(self):
        self.client = APIClient()

        self.admin = Utilisateur.objects.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )

        self.client.force_authenticate(self.admin)

    def test_train_history(self):

        TrainingLog.objects.create(
            dataset_size=100,
            class_distribution={"0": 80, "1": 20},
            accuracy=0.90,
            precision=0.88,
            recall=0.87,
            f1_score=0.87,
            user=self.admin
        )

        response = self.client.get("/predictive/history/")

        assert response.status_code == 200
        assert len(response.data) > 0