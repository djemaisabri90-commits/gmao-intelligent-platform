@patch("predictive.views.predict_all_machines")
def test_machine_risk_list(mock_predict, self):

    mock_predict.return_value = [
        {
            "machine": 1,
            "risk": "HIGH"
        }
    ]

    response = self.client.get(
        "/api/predictive/machine-risk/"
    )

    assert response.status_code == 200
    assert len(response.data) == 1