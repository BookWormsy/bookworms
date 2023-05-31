from django import forms
from .models import UsernamesPasswords, User, Request

class UserForm(forms.ModelForm):
    class Meta:
        model = UsernamesPasswords
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UsernamesPasswords.objects.filter(username=username).exists():
            print("Duplicate username found!")  # Add this line
            raise forms.ValidationError("This username is already in use. Please choose a different username.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UsernamesPasswords.objects.filter(email=email).exists():
            print("Duplicate email found!")  # Add this line
            raise forms.ValidationError("This email is already in use. Please choose a different email.")
        return email


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

class AuthorForm(forms.ModelForm):
    name = forms.CharField(max_length=45)
    surname = forms.CharField(max_length=45)

    class Meta:
        model = UsernamesPasswords
        fields = ['name', 'surname', 'username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UsernamesPasswords.objects.filter(username=username).exists():
            print("Duplicate username found!")  # Add this line
            raise forms.ValidationError("This username is already in use. Please choose a different username.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UsernamesPasswords.objects.filter(email=email).exists():
            print("Duplicate email found!")  # Add this line
            raise forms.ValidationError("This email is already in use. Please choose a different email.")
        return email

class AuthorDetailForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = []

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)