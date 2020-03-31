from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpRequest
from .forms import UserCreationFormWithEmail
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from .models import Mail, MailBox
from django.views.generic import (
	DetailView,
	ListView,
	DeleteView
	)

# Create your views here.
class LoginView (View):
	template_name = 'pages/login.html'
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

class LogoutView (View):
	template_name = 'pages/logout.html'
	def post (self, request, *args, **kwargs):
		logout(request)
		return redirect('welcome')

class RegisterView (View):
	template_name = 'pages/register.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class WelcomeView (View):
	template_name = 'pages/welcome.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class HomeView (View):
	template_name = 'pages/home.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class SignupView (View):
	template_name = 'pages/signup.html'
	def post (self, request, *args, **kwargs):
		form = UserCreationFormWithEmail(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
		else:
			raise ValidationError
			return redirect('create-mailbox')

	def get (self, request, *args, **kwargs):
		form = UserCreationFormWithEmail()
		return render(request, self.template_name, {'form': form})

class ProbaGmaila (View):
	#return HttpResponse(gmail+ssl://tttttttttttttt7@gmail.com%40gmail.com:oauth2@imap.gmail.com?archive=Archived)
	pass

class MailBoxView(ListView):
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
	#success_url = '../../'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def get_success_url(self):
		return reverse('mail:mail-list')

class NotWorkingView (View):
	template_name = 'pages/notworking.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class CreateMailBoxView(View):
	def get(self, request, *args, **kwargs):
		user = request.user
		email = user.email.replace('@gmail.com','')
		data =	{
		'name': email,
		'uri': 'gmail+ssl://' + email + '%40gmail.com:oauth2@imap.gmail.com?archive=Archived',
		'owner': user,
		}
		data_json = JsonResponse(model_to_dict(data))
		url = api_reverse("api-pages:mailbox-create")
		response = requests.post(url, data=data_json)
		if response == status.HTTP_200_OK:
			redirect ('home')
		else:
			redirect('not-working')