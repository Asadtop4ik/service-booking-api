import uuid

from django.db import models

from apps.core.constants import PaymentStatus
from apps.core.models import TimeStampedModel
from apps.order.models import Order


class Payment(TimeStampedModel):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=50, default="fake")
    provider_reference = models.CharField(
        max_length=255, unique=True, default=uuid.uuid4
    )
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    def mark_success(self):
        self.status = PaymentStatus.SUCCESS
        self.save(update_fields=["status", "updated_at"])
        self.order.status = "paid"
        self.order.save(update_fields=["status"])

    def mark_failed(self):
        self.status = PaymentStatus.FAILED
        self.save(update_fields=["status", "updated_at"])
        self.order.status = "canceled"
        self.order.save(update_fields=["status"])
