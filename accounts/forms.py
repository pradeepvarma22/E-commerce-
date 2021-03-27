from django import forms
from ecomApp.models import Product

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price','image')
