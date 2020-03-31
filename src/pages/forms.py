from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class UserCreationFormWithEmail (UserCreationForm):
	email = forms.EmailField(label='Gmail address')

	def save(self, commit=True):
		user = super(UserCreationFormWithEmail, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user