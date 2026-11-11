from django.test import TestCase

# Create your tests here.

from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from stock_movements.models import StockMovement
from stock_movements.services import record_stock_movement


class StockMovementAPITests(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Laptop",
            sku="TEST-LAP-001",
            price=Decimal("750.00"),
            quantity=20,
        )

        self.list_url = reverse("stock-movement-list")

    def test_stock_in_updates_product_quantity(self):
        response = self.client.post(
            self.list_url,
            {
                "product": self.product.id,
                "movement_type": "IN",
                "quantity": 10,
                "notes": "Stock received",
            },
            format="json",
        )

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.product.quantity, 30)
        self.assertEqual(
            StockMovement.objects.count(),
            1,
        )
        self.assertEqual(response.data["product_name"], "Test Laptop")

    def test_stock_out_updates_product_quantity(self):
        response = self.client.post(
            self.list_url,
            {
                "product": self.product.id,
                "movement_type": "OUT",
                "quantity": 5,
                "notes": "Stock issued",
            },
            format="json",
        )

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.product.quantity, 15)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_insufficient_stock_does_not_change_inventory(self):
        response = self.client.post(
            self.list_url,
            {
                "product": self.product.id,
                "movement_type": "OUT",
                "quantity": 100,
                "notes": "Insufficient stock test",
            },
            format="json",
        )

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.product.quantity, 20)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_zero_quantity_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {
                "product": self.product.id,
                "movement_type": "IN",
                "quantity": 0,
                "notes": "Invalid quantity",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_invalid_movement_type_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {
                "product": self.product.id,
                "movement_type": "INVALID",
                "quantity": 5,
                "notes": "Invalid movement",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_stock_movement_cannot_be_updated_or_deleted(self):
        movement = record_stock_movement(
            product_id=self.product.id,
            movement_type=StockMovement.MovementType.STOCK_IN,
            quantity=5,
            notes="Test history",
        )

        detail_url = reverse(
            "stock-movement-detail",
            kwargs={"pk": movement.id},
        )

        update_response = self.client.patch(
            detail_url,
            {"notes": "Modified history"},
            format="json",
        )

        delete_response = self.client.delete(detail_url)

        self.assertEqual(
            update_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertTrue(
            StockMovement.objects.filter(pk=movement.id).exists()
        )
