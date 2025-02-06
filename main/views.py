from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category, Order, Cart, CartItem
from .UserCreationForm import CustomUserCreationForm
from .forms import ProductForm, OrderForm, CartForm
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from main.serializers import ProductSerializer

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse_lazy('main:product_detail', kwargs={'pk': product.pk}))
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect(reverse_lazy('main:order_detail', kwargs={'pk': order.pk}))
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

def create_cart(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:product_list') 
    else:
        form = CartForm()
    return render(request, 'create_cart.html', {'form': form})
def homepage(request):
     products = Product.objects.order_by('-id')[:4]
     categories = Category.objects.all() 
     return render(request, "homepage.html", {"products": products, "categories": categories})

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

class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 50

    def get_queryset(self):
        queryset = Order.objects.all()

        buyer = self.request.GET.get("buyer")
        if buyer:
            queryset = queryset.filter(buyer__username__icontains=buyer)
        min_price = self.request.GET.get("min_total_price")
        if min_price:
            queryset = queryset.filter(total_price__gte=min_price)
        max_price = self.request.GET.get("max_total_price")
        if max_price:
            queryset = queryset.filter(total_price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['title', 'description', 'price', 'stock', 'category', 'image']
    template_name = 'products/product_form.html'

    def get_success_url(self):
        return reverse_lazy('main:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('main:product_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['buyer', 'total_price']
    template_name = 'orders/order_form.html'

    def get_success_url(self):
        return reverse_lazy('main:order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('main:order_list')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("title")
    serializer_class = ProductSerializer
    @method_decorator(login_required) 
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1 
    else:
        cart_item.quantity += 1 
    cart_item.save()

    return redirect('main:cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart) 
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'cart_items': cart_items,'cart_total': cart_total})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('main:cart_detail')