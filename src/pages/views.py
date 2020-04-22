from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ValidationError

from django.views import View
from django.views.generic import (
	CreateView,
	DeleteView,
	DetailView,
	ListView,
	UpdateView,
	)

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
		new_mailbox = MailBox.objects.get_or_create(
			name=email, 
			uri=f'gmail+ssl://{email}%40gmail.com:oauth2@imap.gmail.com?archive=Archived',
			owner=request.user
			)
		return redirect ('home')




#Mail based views
class MailListView(View):
	template_name = 'pages/mail_list.html'
	queryset = None

	def get(self, request, *args, **kwargs):
		mailbox = MailBox.objects.get(
			name=request.user.email.replace('@gmail.com',''),
			owner=request.user
			)
		queryset = Mail.objects.filter(mailbox_id=mailbox.id, spam=False).values()
		return render(request, self.template_name, {'queryset':queryset})

class SpamListView(View):
	template_name = 'pages/mail_list.html'
	queryset = None

	def get(self, request, *args, **kwargs):
		mailbox = MailBox.objects.get(
			name=request.user.email.replace('@gmail.com',''),
			owner=request.user
			)
		queryset = Mail.objects.filter(mailbox_id=mailbox.id, spam=True).values()
		return render(request, self.template_name, {'queryset':queryset})

class MailGetView(ListView):
	template_name = 'pages/get_mail.html'

	def get(self, request, *args, **kwargs):
		creds = None
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json',
					['https://www.googleapis.com/auth/gmail.readonly']
					)
				creds = flow.run_local_server(port=8080)
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		service = build('gmail', 'v1', credentials=creds)
		results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
		messages = results.get('messages', [])

		if messages:
			email = request.user.email.replace('@gmail.com','')
			mailbox = MailBox.objects.get(
				name=email,
				owner=request.user
			)
			for message in messages:
				msg = service.users().messages().get(
					userId='me',
					id=message['id'],
					format="full",
					metadataHeaders=None
					).execute()
				headers_raw = msg['payload']['headers']
				headers = {}
				for header in headers_raw:
					headers[header['name']] = header['value']
				try:
					obj = Mail.objects.get(
						mailbox_id=mailbox.id,
						subject=headers['Subject'],
						from_header=headers['From'],
						to_header=headers['To']
						)
				except Mail.DoesNotExist:
					obj = Mail(
						mailbox_id=mailbox.id,
						subject=headers['Subject'],
						from_header=headers['From'],
						to_header=headers['To'],
						message_id=msg['id'],
						body=msg['payload']['body'],
						#eml=msg['raw'],
						spam=False,
						snippet=msg['snippet']
						)
					obj.save()
					mailbox.received_counter += 1

		return redirect('mail-list')

class MailDetailView(View):
	template_name = 'pages/mail_detail.html'
	queryset = Mail.objects.all()

	#def get(self, request, *args, **kwargs):
	#	mailbox = MailBox.objects.get(
	#		name=request.user.email.replace('@gmail.com',''),
	#		owner=request.user
	#		)
	#	queryset = Mail.objects.filter(mailbox_id=mailbox.id).values()
	#	return render(request, self.template_name, {'queryset':queryset})

class MailDeleteView(DeleteView):
	template_name = 'pages/mail_delete.html'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def get_success_url(self):
		return reverse('mail:mail-list')