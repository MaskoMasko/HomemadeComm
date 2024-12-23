from django import forms
from .models import Product, Order, Cart

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['seller', 'title', 'description', 'price', 'stock', 'image', 'category']

    # image set to optional, cause i dont like uploading mediaimages
    image = forms.ImageField(required=False)

    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'min': '0'}),
        min_value=0,
        max_digits=10,
        decimal_places=2
    )

    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '0'}),
        min_value=0
    )

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer', 'total_price']

    total_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'min': '0'}),
        min_value=0,
        max_digits=10,
        decimal_places=2
    )

    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price < 0:
            raise forms.ValidationError("Total price cannot be negative.")
        return total_price


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
