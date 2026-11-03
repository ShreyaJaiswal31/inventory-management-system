from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Product price must be greater than zero."
            )

        return value