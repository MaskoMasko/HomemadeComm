from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name='index'),
    path("register/",views.register, name="register"),
    path("admin-only/", views.admin_only_view, name="admin_only"),
]