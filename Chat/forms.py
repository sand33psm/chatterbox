from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rechat


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150, 
        help_text='',
        label='',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        max_length=150, 
        help_text='',
        label='',
        widget=forms.EmailInput(attrs={
            'class': "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400",
            'placeholder': 'Email Address'
        })
    )
    password1 = forms.CharField(
        max_length=150, 
        help_text='',
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        max_length=150, 
        help_text='',  # Remove help text
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Remove unwanted fields
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
