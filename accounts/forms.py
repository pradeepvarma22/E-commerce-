from django import forms
from ecomApp.models import Product

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_price','product_image')
