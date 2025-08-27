from rest_framework import permissions, viewsets

from apps.order.models import Order
from apps.order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all()
        if user.role == "worker":
            return Order.objects.filter(worker=user)
        return Order.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
