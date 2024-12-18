from django.urls import path
from .views import ProductListView, homepage, register, admin_only_view,ProductDetailView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path("", homepage, name='index'),
    path("register/",register, name="register"),
    path("admin-only/", admin_only_view, name="admin_only"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)