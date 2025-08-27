from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .payment import PaymentViewSet

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]

__all__ = ["urlpatterns"]
