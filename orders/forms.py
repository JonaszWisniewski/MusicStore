from django import forms
from .models import Order
from djmoney.forms.fields import MoneyField

var_class = 'w-full py-4 px-6 rounded-xl border'

class AddressUpdateForm(forms.ModelForm):
  
    class Meta:
        model = Order
        fields = ['age','country','address1', 'address2', 'city','county','phone','full_name']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': var_class
            }),
            'age': forms.TextInput(attrs={
                'class': var_class
            }),
            'address1': forms.TextInput(attrs={
                'class': var_class
            }),
            'address2': forms.TextInput(attrs={
                'class': var_class
            }),
            'country': forms.TextInput(attrs={
                'class': var_class
            }),
            'city': forms.TextInput(attrs={
                'class': var_class
            }),
            'county': forms.TextInput(attrs={
                'class': var_class
            }),
            'phone': forms.TextInput(attrs={
                'class': var_class
            })}