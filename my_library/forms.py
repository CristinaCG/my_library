from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(forms.ModelForm):
    """
    Form for registering a new user.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': 'Type your password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Type your password again'}))

    class Meta:
        """
        Meta class for UserRegisterForm.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Type your user name'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Type your first name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Type your last name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Type your email address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
