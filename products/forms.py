from django import forms
from .models import Product
from djmoney.forms.fields import MoneyField


var_holding_class = 'w-full py-4 px-6 rounded-xl border'

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'price', 'description', 'image')

        widgets = {
            'category': forms.Select(attrs={
                'class': var_holding_class
            }),
            'name': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'description': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'image': forms.FileInput(attrs={
                'class': var_holding_class
            }),
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','description','price','image','is_sold')
        
        price = MoneyField(disabled=True)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'description': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'image': forms.FileInput(attrs={
                'class': var_holding_class
            })
        }

class CouponCodeForm(forms.Form):
    code = forms.CharField(required=False)



class AddRatingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('rating',)
        







    