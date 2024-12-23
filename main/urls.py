from django.urls import path
from .views import ProductListView, homepage,OrderListView,OrderDetailView, register, admin_only_view,ProductDetailView, create_cart, create_order, create_product
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path("", homepage, name='index'),
    path("register/",register, name="register"),
    path("admin-only/", admin_only_view, name="admin_only"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path('create/product/', create_product, name='create_product'),
    path('create/order/', create_order, name='create_order'),
    path('create/cart/', create_cart, name='create_cart'),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)