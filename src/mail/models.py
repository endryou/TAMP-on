from django.db import models

# Create your models here.
class Mail (models.Model):
	mail_from = models.CharField(max_length=40)
	mail_to = models.CharField(max_length=40)
	mail_title = models.CharField(max_length=40)
	mail_text = models.TextField()

	def get_absolute_url(self):
		return reverse("mail:mail-detail", kwargs={"pk": self.pk})