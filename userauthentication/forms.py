from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User, Profile


class UserRegisterForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Full Name", 'class':"a custom class"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your User Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Number"}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Password"}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Comfirm your Password"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']

class UserHotelRegisterForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Full Name", 'class':"a custom class"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your User Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your  Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your  Number"}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Password"}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Comfirm your Password"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']