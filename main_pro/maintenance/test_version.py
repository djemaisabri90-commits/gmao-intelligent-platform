def test_train_history_detail(self):

    log = TrainingLog.objects.create(
        dataset_size=100,
        class_distribution={"0": 80, "1": 20},
        accuracy=0.91,
        precision=0.90,
        recall=0.89,
        f1_score=0.89,
        user=self.admin
    )

    response = self.client.get(
        f"/api/predictive/history/{log.model_version}/"
    )

    assert response.status_code == 200
    assert response.data["model_version"] == log.model_version