from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	def get (self, request, *args, **kwargs):
		form = UserCreationForm()
		return render(request, self.template_name, {'form': form})