from rest_framework import serializers
from main.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = ("id", "seller", "title", "description", "price", "stock", "image", "category", )