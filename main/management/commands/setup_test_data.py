import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import Category, Product, Order, OrderItem, Cart, CartItem
from main.factory import CategoryFactory, ProductFactory, OrderFactory, OrderItemFactory, CartFactory, CartItemFactory

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Category, Product, Order, OrderItem, Cart, CartItem]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(10):
            category = CategoryFactory()
            product = ProductFactory()
            order = OrderFactory()
            orderItem = OrderItemFactory()
            cart = CartFactory()
            cartItem = CartItemFactory()