from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import ClothingItem

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40,required= True,help_text=None)
    last_name = forms.CharField(max_length=30,required= True, help_text= None)
    username = forms.CharField(max_length = 20,required= True, help_text = None)
    email = forms.EmailField(max_length = 254,required = True,help_text='Please type a valid email')
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField()

class ClothingItemForm(forms.ModelForm):    
    class Meta:
        model = ClothingItem
        fields = ('user','category','name','image')
