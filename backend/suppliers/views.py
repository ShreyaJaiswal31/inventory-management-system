from django.shortcuts import render
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("-id")
    serializer_class = SupplierSerializer