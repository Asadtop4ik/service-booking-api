from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "workers",
            {
                "type": "notify",
                "payload": {
                    "message": f"New order created: {instance.id}",
                    "order_id": instance.id,
                    "status": instance.status,
                },
            },
        )

        async_to_sync(channel_layer.group_send)(
            f"client_{instance.client_id}",
            {
                "type": "notify",
                "payload": {
                    "message": f"Your order {instance.id} was created!",
                    "order_id": instance.id,
                    "status": instance.status,
                },
            },
        )
