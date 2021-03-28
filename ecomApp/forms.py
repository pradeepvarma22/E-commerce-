from django import forms
from ecomApp.models import Checkout




class OrderForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields=('fullname','email','NameOnCard','Address','creditcardnumber','city','cardExpdate','state','zip','cvv')
