from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITests(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Dell Laptop",
            sku="LAP-DELL-001",
            description="Business laptop",
            price="1299.99",
            quantity=25,
            reorder_level=10,
            is_active=True
        )

        self.list_url = reverse("product-list")
        self.detail_url = reverse(
            "product-detail",
            kwargs={"pk": self.product.pk}
        )

    def test_get_products(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        data = {
            "name": "HP Laptop",
            "sku": "LAP-HP-001",
            "description": "HP business laptop",
            "price": "899.99",
            "quantity": 15,
            "reorder_level": 5,
            "is_active": True
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Product.objects.count(), 2)

    def test_reject_zero_price(self):
        data = {
            "name": "Invalid Laptop",
            "sku": "LAP-INVALID-001",
            "price": "0",
            "quantity": 10,
            "reorder_level": 2,
            "is_active": True
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_reject_duplicate_sku(self):
        data = {
            "name": "Another Dell Laptop",
            "sku": "LAP-DELL-001",
            "price": "500.00",
            "quantity": 10,
            "reorder_level": 2,
            "is_active": True
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_update_product_quantity(self):
        data = {"quantity": 50}

        response = self.client.patch(
            self.detail_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 50)