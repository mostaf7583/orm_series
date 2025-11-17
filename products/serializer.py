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
    def validate(self, data):
        parent = data.get('parent')
        # On update, self.instance exists
        if parent and self.instance and parent == self.instance:
            raise serializers.ValidationError("A category cannot be its own parent")
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    def validate(self, data):
        parent = data.get('parent')
        # On update, self.instance exists
        if parent and self.instance and parent == self.instance:
            raise serializers.ValidationError("A category cannot be its own parent")
        return data
