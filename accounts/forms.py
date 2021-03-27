from django import forms
from ecomApp.models import Product


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user',)
        fields=('name','price','image')

        widgets = {
            'image': forms.widgets.FileInput
        }


