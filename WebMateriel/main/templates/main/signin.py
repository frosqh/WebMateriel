from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20, label='Nom')
	password = forms.CharField(widget=forms.PasswordInput, label='Password')

	def clean(self):
		cleaned_data = super(LoginForm,self).clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")