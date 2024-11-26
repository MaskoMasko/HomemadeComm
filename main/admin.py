from django.contrib import admin
from .models import User, Product, Cart, CartItem, Category, Order, OrderItem

# Register your models here.
admin.site.register([User, Product, Category, CartItem, Cart, Order, OrderItem])