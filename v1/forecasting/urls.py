from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import update_forecasting

router = DefaultRouter()
router.register("forecastings", views.ForecastingViewSet)

urlpatterns = [
    path("manual-update/", update_forecasting, name="update_forecasting"),
    path("", include(router.urls)),
]
