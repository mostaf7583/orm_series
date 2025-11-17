from asgiref.sync import sync_to_async
from django.db import transaction
from django.shortcuts import render

# Create your views here.
# Python
from rest_framework import generics
from rest_framework.response import Response

from products.models import Product
from products.serializer import ProductSerializer, CategorySerializer
from django.db import transaction
from asgiref.sync import sync_to_async
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import (Product, Category)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from products.models import Product, Category
from products.serializer import ProductSerializer, CategorySerializer


class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET  /products/        -> list all products
    POST /products/        -> create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        category = serializer.validated_data.get('category')
        if category is None:
            raise ValidationError({"category": "Category must be specified"})
        serializer.save()


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /products/<pk>/ -> retrieve one product
    PUT    /products/<pk>/ -> full update
    PATCH  /products/<pk>/ -> partial update
    DELETE /products/<pk>/ -> delete
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_update(self, serializer):
        category = serializer.validated_data.get('category')
        if category is None:
            raise ValidationError({"category": "Category must be specified"})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.stock > 0:
            raise ValidationError({"detail": "Cannot delete a product with stock remaining"})
        instance.delete()


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET  /Category/        -> list all Category
    POST /Category/        -> create a new Category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        parent = serializer.validated_data.get('parent')
        if parent and parent == serializer.validated_data.get('id'):
            raise ValidationError({"parent": "A category cannot be its own parent"})
        serializer.save()


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /categories/<pk>/ -> retrieve one category
    PUT    /categories/<pk>/ -> full update
    PATCH  /categories/<pk>/ -> partial update
    DELETE /categories/<pk>/ -> delete
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance):
        if instance.products.exists():
            raise ValidationError({"detail": "Cannot delete a category that has products"})
        instance.delete()


class CategoryAsSlug(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        if instance.products.exists():
            raise ValidationError({"detail": "Cannot delete a category that has products"})
        instance.delete()


class CategoryProductListView(generics.ListAPIView):
    """
    GET /products/categories/<slug:category_slug>/products/ -> List all products in a specific category
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        try:
            category = Category.objects.get(slug=category_slug)
            return Product.objects.filter(category=category)
        except Category.DoesNotExist:
            raise ValidationError({"detail": f"Category with slug '{category_slug}' does not exist"})

"""
For Products :
1.view all Products
2.view one Product
3.create a new Product
4.update a Product
5.delete a Product
6.link a Product to a Category
7.view all Products in a Category

"""
