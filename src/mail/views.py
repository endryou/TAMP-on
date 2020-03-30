from django.contrib.auth.models import User
from .models import Mail
from django.shortcuts import render
from django.views.generic import (
	DetailView,
	ListView,
	DeleteView
	)

# Create your views here.
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

class MailBoxView2(ListView):
	template_name = 'mail/mail_list.html'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		user = request.user
		if user.is_authenticated:
			if user.email is not None:
				pass
		return render(request, self.template_name)