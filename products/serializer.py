from rest_framework import serializers
from unicodedata import category

from products.models import Product, Category


# In Django REST Framework (DRF), a Serializer is a component that
# converts complex data—such as Django model instances,
# querysets, or Python objects—into JSON, a
# nd also converts JSON input back into Python data.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields in the model

    def create(self, validated_data):
        # If a list of items was passed → bulk create
        if isinstance(validated_data, list):
            return Product.objects.bulk_create([Product(**item) for item in validated_data])

        # Single object
        return Product.objects.create(**validated_data)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
