from django.contrib.auth import get_user_model
from django.db import models

from apps.core.constants import OrderStatus
from apps.core.models import TimeStampedModel

User = get_user_model()


class Order(TimeStampedModel):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client_orders"
    )
    worker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="worker_orders",
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )

    def __str__(self):
        return f"Order #{self.id} - {self.client.username} - {self.status}"
