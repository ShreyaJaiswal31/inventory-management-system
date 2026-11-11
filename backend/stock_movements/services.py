# We'll use Django's transaction.atomic() and select_for_update() to protect inventory updates from concurrent requests.

from django.db import transaction
from django.core.exceptions import ValidationError

from products.models import Product
from .models import StockMovement


@transaction.atomic
def record_stock_movement(product_id, movement_type, quantity, notes=""):

    # Validate movement type
    if movement_type not in StockMovement.MovementType.values:
        raise ValidationError("Invalid stock movement type.")

    # Validate quantity
    if quantity < 1:
        raise ValidationError("Quantity must be greater than zero.")

    # Lock the product row to prevent concurrent inventory updates
    product = Product.objects.select_for_update().get(pk=product_id)

    # Calculate the new inventory quantity
    if movement_type == StockMovement.MovementType.STOCK_IN:
        product.quantity += quantity

    elif movement_type == StockMovement.MovementType.STOCK_OUT:

        if product.quantity < quantity:
            raise ValidationError(
                f"Insufficient stock. Available quantity: {product.quantity}."
            )

        product.quantity -= quantity

    # Save the updated product quantity
    product.save(update_fields=["quantity", "updated_at"])

    # Create the stock movement history record
    movement = StockMovement.objects.create(
        product=product,
        movement_type=movement_type,
        quantity=quantity,
        notes=notes
    )

    return movement