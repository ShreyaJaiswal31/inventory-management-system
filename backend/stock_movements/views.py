from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import StockMovement
from .serializers import StockMovementSerializer
from .services import record_stock_movement


class StockMovementViewSet(viewsets.ModelViewSet):

    queryset = StockMovement.objects.select_related(
        "product"
    ).all().order_by("-id")

    serializer_class = StockMovementSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            movement = record_stock_movement(
                product_id=data["product"].id,
                movement_type=data["movement_type"],
                quantity=data["quantity"],
                notes=data.get("notes", "")
            )

        except Exception as exc:
            from django.core.exceptions import ValidationError as DjangoValidationError

            if isinstance(exc, DjangoValidationError):
                raise ValidationError(exc.messages)

            raise

        output_serializer = self.get_serializer(movement)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        raise ValidationError(
            "Stock movements cannot be updated. Create a new movement instead."
        )

    def partial_update(self, request, *args, **kwargs):
        raise ValidationError(
            "Stock movements cannot be updated. Create a new movement instead."
        )

    def destroy(self, request, *args, **kwargs):
        raise ValidationError(
            "Stock movements cannot be deleted."
        )