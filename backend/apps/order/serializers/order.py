from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.order.models import Order

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)
    worker = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "client", "worker", "description", "price", "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["client"] = request.user
        return super().create(validated_data)
