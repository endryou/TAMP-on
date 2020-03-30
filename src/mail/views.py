from .models import Mail
from django.shortcuts import render
from django.views.generic import (
	DetailView,
	ListView,
	DeleteView
	)

# Create your views here.
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
	#success_url = '../../'
	queryset = Mail.objects.all()

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def get_success_url(self):
		return reverse('mail:mail-list')