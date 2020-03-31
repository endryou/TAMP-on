from django_mailbox.models import Mailbox, Message
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse


# Create your models here.
class MailBox (Mailbox):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def get_api_url(self, request=None):
		return api_reverse("api-pages:mailbox-create", kwargs={'pk': self.pk}, request=request)

class Mail(Message):
	pass