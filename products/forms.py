from django import forms
from .models import Product

var_holding_class = 'w-full py-4 px-6 rounded-xl border'

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name','description','price','image')

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
            'price': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'image': forms.FileInput(attrs={
                'class': var_holding_class
            })
        }

    

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','description','price','image','is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'description': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'price': forms.TextInput(attrs={
                'class': var_holding_class
            }),
            'image': forms.FileInput(attrs={
                'class': var_holding_class
            })
        }

class CouponCodeForm(forms.Form):
    code = forms.CharField(required=False)

    