from model_bakery import baker
import pytest


@pytest.fixture
def forecasting_batch():
    def forecasting_bakery_batch(n):
        forecasting_factory = baker.make(
            'forecasting.Forecasting',
            _fill_optional=[
                'date',
                'sigungu_code',
                'sigungu_name',
                'crop_name',
                'crop_code',
                'target'
            ],
            _quantity=n
        )
        return forecasting_factory
    return forecasting_bakery_batch
