import factory
from factory.django import DjangoModelFactory
from .models import User, Product, Category, Order, OrderItem, Cart, CartItem

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    is_seller = factory.Faker('boolean', chance_of_getting_true=30)  # 30% chance of being a seller
    is_buyer = factory.LazyAttribute(lambda obj: not obj.is_seller)  # Inverse of is_seller

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    description = factory.Faker('sentence')

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    seller = factory.SubFactory(UserFactory, is_seller=True)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=3)
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=1, max=100)
    image = factory.django.ImageField(filename='test_image.jpg')
    category = factory.SubFactory(CategoryFactory)
    created_at = factory.Faker('date_time_this_year')


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    buyer = factory.SubFactory(UserFactory, is_seller=False)
    created_at = factory.Faker('date_time_this_year')
    total_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)

class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory, is_seller=False)

class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
