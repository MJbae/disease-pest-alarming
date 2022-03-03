from model_bakery import baker
import json
import pytest

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestForecastingEndpoints:
    endpoint = '/api/v1/forecasting/forecastings/'

    def test_list(self, api_client, forecasting_batch):
        forecasting_batch(3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3
