import uuid

from rest_framework import serializers

from apps.core.constants import DomainException
from apps.order.serializers import OrderSerializer
from apps.payment.models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    provider = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "order", "amount", "provider"]

    def validate_order(self, value):
        request = self.context["request"]
        if request.user != value.client and request.user.role != "admin":
            raise DomainException(1007)
        if value.status != "pending":
            raise DomainException(1008)
        return value

    def create(self, validated_data):
        order = validated_data["order"]
        validated_data["amount"] = order.price
        validated_data["provider_reference"] = str(uuid.uuid4())
        payment = Payment.objects.create(**validated_data)
        return payment


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "provider",
            "provider_reference",
            "status",
            "created_at",
        ]
        read_only_fields = fields
