from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.constants import DomainException
from apps.payment.models import Payment
from apps.payment.serializers import PaymentCreateSerializer, PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"], url_path="success")
    def mark_success(self, request, pk=None):
        payment = self.get_object()
        if payment.status != "pending":
            raise DomainException(1009)
        payment.mark_success()
        data = PaymentSerializer(payment).data
        data.update({"message": "Payment marked as SUCCESS"})
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="fail")
    def mark_failed(self, request, pk=None):
        payment = self.get_object()
        if payment.status != "pending":
            raise DomainException(1009)
        payment.mark_failed()
        data = PaymentSerializer(payment).data
        data.update({"message": "Payment marked as FAILED"})
        return Response(data, status=status.HTTP_200_OK)
