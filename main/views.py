from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category
from .UserCreationForm import CustomUserCreationForm

def homepage(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def is_admin_user(user):
    return user.is_staff

@login_required
def admin_only_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, "admin_only.html")



class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 100

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        seller = self.request.GET.get("seller")
        if seller:
            queryset = queryset.filter(seller__name__icontains=seller)
        min_price = self.request.GET.get("min_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.GET.get("max_price")
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html" 
    context_object_name = "product"