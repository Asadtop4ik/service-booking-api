from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.order.models import Order
from apps.order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all()
        if user.role == "worker":
            return Order.objects.filter(worker=user)
        return Order.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        """
        Worker buyurtmani qabul qiladi.
        Rules: faqat role=worker, order.pending bo'lsa, worker set qilinadi, status 'accepted' (yoki siz nimani xohlasangiz).
        So'ng client guruhiga real-time xabar yuboriladi: ORDER_ACCEPTED
        """
        user = request.user
        if getattr(user, "role", None) != "worker":
            return Response({"detail": "Only workers can accept orders."}, status=403)

        order = self.get_object()
        if order.status not in ("pending", "created"):
            return Response({"detail": "Order is not available to accept."}, status=400)
        if order.worker_id:
            return Response({"detail": "Order already assigned."}, status=400)

        # assign worker + status
        order.worker = user
        order.status = "accepted"
        order.save(update_fields=["worker", "status"])

        # clientga real-time xabar
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"client_{order.client_id}",
            {
                "type": "notify",
                "payload": {
                    "event": "ORDER_ACCEPTED",
                    "order_id": order.id,
                    "status": order.status,
                    "worker_id": user.id,
                },
            },
        )

        return Response(OrderSerializer(order).data, status=200)
