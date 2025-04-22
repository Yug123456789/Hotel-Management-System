from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User, Profile


class UserRegisterForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Full Name", 'class': "a custom class"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your User Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Number"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter your Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm your Password"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user

    
class UserHotelRegisterForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Full Name", 'class': "a custom class"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your User Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Email"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your Number"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter your Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm your Password"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'hotel'
        if commit:
            user.save()
        return user