from django.urls import path
from .views import ProductListView, homepage, register, admin_only_view,ProductDetailView

app_name = 'main'

urlpatterns = [
    path("", homepage, name='index'),
    path("register/",register, name="register"),
    path("admin-only/", admin_only_view, name="admin_only"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:pk>/", ProductDetailView.as_view(), name="product_detail"),
]