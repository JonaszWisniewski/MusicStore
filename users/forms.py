from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

var_class = "w-full rounded-xl py-3 px-5"

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']



    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': var_class})
        self.fields['password'].widget = forms.TextInput(attrs={'class': var_class,
                                                                     'type': 'password'})
      

class SignUpForm(UserCreationForm):
    age = forms.CharField(max_length=4, required=True)
    country = forms.CharField(max_length=30, required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'age', 'country')
    
        widgets = {
            'username': forms.TextInput(attrs={
                'class': var_class
            }),
            'email': forms.TextInput(attrs={
                'class': var_class
            })}
        
    def __init__(self, *args, **kwargs): # function to make password1 and password2 hide the password
            super(UserCreationForm, self).__init__(*args, **kwargs)
            self.fields['password1'].widget = forms.TextInput(attrs={'class': var_class,
                                                                        'type': 'password'})
            self.fields['password2'].widget = forms.TextInput(attrs={'class': var_class,
                                                                        'type': 'password'}) 
        
    age = forms.CharField(widget=forms.TextInput(attrs={'class': var_class}))  
    country = forms.CharField(widget=forms.TextInput(attrs={'class': var_class}))
        
        
    
    def save(self, commit=True):
        user=super(SignUpForm, self).save(commit=False)
        user.age = self.cleaned_data["age"]
        user.country = self.cleaned_data["country"]
        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'username']

        widgets = {
            'email': forms.TextInput(attrs={
                'class': var_class
            }),
            'username': forms.TextInput(attrs={
                'class': var_class,
                'disabled': True #disabled by default so that it cannot be changed
                
            })
            }
        
    def save(self, commit=True):
        user=super(UserUpdateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user    
        

class ProfileUpdateForm(forms.ModelForm):
    # image = forms.ImageField(widget=forms.FileInput) # removes the path to the image
    class Meta:
        model = Profile
        fields = ['age','country','address1', 'address2','image', 'city','county','phone','full_name']

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
            }),
            'image': forms.FileInput(attrs={
                'class': 'py-4'
            })}

class PasswordForm(PasswordChangeForm): # overwriting the PasswordForm so that widgets can be customized
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.TextInput(attrs={'class': var_class,
                                                                    'type': 'password'})
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class': var_class,
                                                                     'type': 'password'})
        del self.fields['new_password2'] # deletes the confirmation password
        



    

