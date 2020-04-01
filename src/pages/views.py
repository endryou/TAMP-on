from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.views import View
from django.views.generic import (
	CreateView,
	DeleteView,
	DetailView,
	ListView,
	UpdateView,
	)

from rest_framework import status
from rest_framework.reverse import reverse as api_reverse

from .models import Mail, MailBox
from .forms import UserCreationFormWithEmail, UserUpdateForm


# User based views
class UserLoginView (View):
	template_name = 'pages/user_login.html'
	def post (self, request, *args, **kwargs):
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
		else:
			return redirect('welcome')
	def get (self, request, *args, **kwargs):
		form = AuthenticationForm()
		return render(request, self.template_name, {'form': form})

class UserLogoutView (View):
	def post (self, request, *args, **kwargs):
		logout(request)
		return redirect('welcome')

class UserUpdateView (View):
	template_name = 'pages/user_update.html'
	model = User
	success_url = 'pages/user_update.html'
	def post (self, request, *args, **kwargs):
		form = UserUpdateForm(data=request.POST, instance=request.user)
		form.fields['first_name'].initial = request.user.first_name
		form.fields['last_name'].initial = request.user.last_name
		form.fields['email'].initial = request.user.email
		if form.is_valid():
			form.save()
		return redirect('home')
	def get(self, request, *args, **kwargs):
		form = UserUpdateForm()
		form.fields['first_name'].initial = request.user.first_name
		form.fields['last_name'].initial = request.user.last_name
		form.fields['email'].initial = request.user.email
		return render(request, self.template_name, {'form': form})	

class UserDeleteView (DeleteView):
	template_name = 'pages/user_delete.html'
	def get (self, request, *args, **kwargs):
		return render(request, self.template_name, {})
	def post(self, request, *args, **kwargs):
		user = User.objects.get(pk=request.user.pk)
		user.delete()
		return redirect('welcome') 

class UserSignupView (View):
	template_name = 'pages/user_signup.html'
	def post (self, request, *args, **kwargs):
		form = UserCreationFormWithEmail(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('create-mailbox')
		else:
			raise ValidationError

	def get (self, request, *args, **kwargs):
		form = UserCreationFormWithEmail()
		return render(request, self.template_name, {'form': form})
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class UserChangePassword(View):
	template_name = 'pages/user_change_password.html'
	def post (self, request, *args, **kwargs):
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			return redirect('home')
	def get (self, request, *args, **kwargs):
		form = PasswordChangeForm(request.user)
		return render(request, self.template_name, {'form': form})






#Main views
class WelcomeView (View):
	template_name = 'pages/welcome.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class HomeView (View):
	template_name = 'pages/home.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class NotWorkingView (View):
	template_name = 'pages/notworking.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)






#MailBox based views
class CreateMailBoxView(View):
	def get(self, request, *args, **kwargs):
		email = request.user.email.replace('@gmail.com','')
		new_mailbox = MailBox.objects.create(
			name=email, 
			uri=f'gmail+ssl://{email}%40gmail.com:oauth2@imap.gmail.com?archive=Archived',
			owner=request.user
			)
		return redirect ('home')




#Mail based views
class MailListView(ListView):
	template_name = 'mail/mail_list.html'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class MailDetailView(DetailView):
	template_name = 'mail/mail.html'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class MailDeleteView(DeleteView):
	template_name = 'mail/mail_delete.html'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def get_success_url(self):
		return reverse('mail:mail-list')