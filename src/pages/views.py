from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .forms import UserCreationFormWithEmail
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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

class CreateMailBoxView(View):
	pass