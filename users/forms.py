from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
	location = forms.CharField(widget=forms.Textarea, help_text='Required')
	city = forms.CharField(help_text='Required')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
	
class UserEditForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
	location = forms.CharField(widget=forms.Textarea, help_text='Required')
	city = forms.CharField(help_text='Required')

	class Meta:
		model = Profile
		fields = ('location', 'city')
