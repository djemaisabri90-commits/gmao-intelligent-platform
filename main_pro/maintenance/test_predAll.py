import pytest
from unittest.mock import patch

from rest_framework.test import APIClient

from maintenance.models import Utilisateur, Machine
from predictive.models import TrainingLog

pytestmark = pytest.mark.django_db


class TestPredictiveAPI:

    def setup_method(self):

        self.client = APIClient()

        self.admin = Utilisateur.objects.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )

        self.expert = Utilisateur.objects.create_user(
            username="expert",
            password="expert123",
            role="expert"
        )

        self.client.force_authenticate(self.admin)

    # =====================================================
    # TRAIN HISTORY
    # =====================================================

    def test_train_history(self):

        print("\n==============================")
        print("Scénarion de test :\nConsultation historique des entraînements")
        print("==============================")

        log=TrainingLog.objects.create(
            dataset_size=100,
            class_distribution={"0": 80, "1": 20},
            balanced_distribution={"0": 80, "1": 80},
            accuracy=0.95,
            precision=0.94,
            recall=0.93,
            f1_score=0.93,
            user=self.admin
        )

        print(f"Version créée : {log.model_version}")

        response = self.client.get(
            "/predictive/train-history/"
        )

        print(f"Code retour : {response.status_code}")
        print(f"Nombre de logs retournés : {len(response.data)}")
        
        assert response.status_code == 200
        assert len(response.data) == 1

        print("Test réussi!!")

    # =====================================================
    # LATEST TRAIN HISTORY
    # =====================================================

    def test_latest_train_history(self):

        log = TrainingLog.objects.create(
            dataset_size=200,
            class_distribution={"0": 150, "1": 50},
            accuracy=0.96,
            precision=0.95,
            recall=0.94,
            f1_score=0.94,
            user=self.admin
        )

        response = self.client.get(
            "/predictive/train-history/latest/"
        )

        assert response.status_code == 200
        assert response.data["model_version"] == log.model_version

    # =====================================================
    # TRAIN HISTORY DETAIL
    # =====================================================

    def test_train_history_detail(self):

        log = TrainingLog.objects.create(
            dataset_size=300,
            class_distribution={"0": 240, "1": 60},
            accuracy=0.92,
            precision=0.91,
            recall=0.90,
            f1_score=0.90,
            user=self.admin
        )

        response = self.client.get(
            f"/predictive/train-history/{log.model_version}/"
        )

        assert response.status_code == 200
        assert response.data["accuracy"] == log.accuracy

    # =====================================================
    # TRAIN MODEL
    # =====================================================

    @patch("predictive.views.train")
    def test_train_ai_model(self, mock_train):

        print("\n==============================")
        print("Scénarion de test :\nRéentraînement du modèle IA")
        print("==============================")

        mock_train.return_value = {
            "success": True,
            "accuracy": 0.97
        }
        response = self.client.post(
            "/predictive/train/",
            {
                "scratch": True,
                "minority_ratio": 0.3
            },
            format="json"
        )
        print(f"Code retour : {response.status_code}")
        print(f"Réponse : {response.data}")
        assert response.status_code == 200
        assert "message" in response.data
        print("Réentraînement validé!!")
    # =====================================================
    # EXPORT JSON
    # =====================================================
    def test_export_log_json(self):

        print("\n==============================")
        print("Scénarion de test :\nExport JSON")
        print("==============================")
        log = TrainingLog.objects.create(
            dataset_size=120,
            class_distribution={"0": 90, "1": 30},
            accuracy=0.90,
            precision=0.89,
            recall=0.88,
            f1_score=0.88,
            user=self.admin
        )
        response = self.client.get(
            f"/predictive/export/{log.model_version}/json/"
        )
        print(f"Version exportée : {log.model_version}")
        print(f"Content-Type : {response['Content-Type']}")
        assert response.status_code == 200
    # =====================================================
    # EXPORT CSV
    # =====================================================

    def test_export_log_csv(self):
        print("\n==============================")
        print("Scénarion de test :\nExport CSV")
        print("==============================")

        log = TrainingLog.objects.create(
            dataset_size=120,
            class_distribution={"0": 90, "1": 30},
            accuracy=0.90,
            precision=0.89,
            recall=0.88,
            f1_score=0.88,
            user=self.admin
        )

        response = self.client.get(
            f"/predictive/export/{log.model_version}/csv/"
        )
        print(f"Version exportée : {log.model_version}")
        print(f"Content-Type : {response['Content-Type']}")
        assert response.status_code == 200

        assert (
            response["Content-Type"]
            == "text/csv"
        )
        print("Export CSV réussi!!")

    # =====================================================
    # EXPORT XLSX
    # =====================================================

    def test_export_log_xlsx(self):
        print("\n==============================")
        print("Scénarion de test :\nExport XLSX")
        print("==============================")

        log = TrainingLog.objects.create(
            dataset_size=120,
            class_distribution={"0": 90, "1": 30},
            accuracy=0.90,
            precision=0.89,
            recall=0.88,
            f1_score=0.88,
            user=self.admin
        )

        response = self.client.get(
            f"/predictive/export/{log.model_version}/xlsx/"
        )
        print(f"Version exportée : {log.model_version}")
        print(f"Content-Type : {response['Content-Type']}")
        assert response.status_code == 200
        print("Export XLSX réussi!!")

    # =====================================================
    # MACHINE RISK LIST
    # =====================================================

    @patch("predictive.views.predict_all_machines")
    def test_machine_risk_list(self, mock_predict):
        print("\n==============================")
        print("Scénarion de test :\nVisualisation des risques machines")
        print("==============================")

        mock_predict.return_value = [
            {
                "machine": 1,
                "risk": "HIGH"
            }
        ]

        response = self.client.get(
            "/predictive/machine-risk/"
        )
        print(f"Code retour : {response.status_code}")
        print(f"Données : {response.data}")
        assert response.status_code == 200
        assert len(response.data) == 1
        print("Prédictions récupérées!!")

    # =====================================================
    # MACHINE RISK DETAIL
    # =====================================================

    @patch("predictive.views.predict_machine")
    def test_machine_risk_detail(self, mock_predict):
        print("\n==============================")
        print("Scénarion de test :\nVisualiser risque d'une machine")
        print("==============================")

        machine = Machine.objects.create(
            nom="Machine Test"
        )

        mock_predict.return_value = {
            "machine": machine.id,
            "risk": "MEDIUM"
        }

        response = self.client.get(
            f"/predictive/machine-risk/{machine.id}/"
        )

        assert response.status_code == 200
        assert response.data["risk"] == "MEDIUM"
        print("Prédiction du risque d'une machine récupéré")

    from unittest.mock import patch

    @patch("predictive.views.joblib.load")
    @patch("predictive.views.os.path.exists")
    def test_list_features(self, mock_exists, mock_load):
        print("\n==============================")
        print("Scénarion de test :\nVisualiser liste des features d'entraînement")
        print("==============================")
        

        mock_exists.return_value = True

        mock_load.return_value = [
            "total_interventions",
            "validated_interventions"
        ]

        response = self.client.get(
            "/predictive/features/"
        )
        print("\nConsultation des features utilisées réussie")
        assert response.status_code == 200