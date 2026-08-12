from unittest.mock import patch

@patch("predictive.views.train")
def test_train_model(mock_train, self):

    mock_train.return_value = {
        "success": True,
        "accuracy": 0.95
    }

    response = self.client.post(
        "/api/predictive/train/",
        {
            "scratch": True
        },
        format="json"
    )

    assert response.status_code == 200
    assert "message" in response.data