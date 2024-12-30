from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = NotesUser
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = make_password(password)
        return super().save(commit=commit)

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'content')

class LoginForm(forms.Form):
    LOGIN_CHOICES = [
        ('username', 'Username'),
        ('email', 'Email'),
    ]
    
    login_type = forms.ChoiceField(choices=LOGIN_CHOICES, widget=forms.RadioSelect, required=True)
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        login_type = cleaned_data.get('login_type')
        if login_type == 'username' and not cleaned_data.get('username'):
            self.add_error('username', 'Username is required.')
        elif login_type == 'email' and not cleaned_data.get('email'):
            self.add_error('email', 'Email is required.')        
        return cleaned_data