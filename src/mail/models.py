from django_mailbox.models import Mailbox, Message

# Create your models here.
class MailBox (Mailbox):
	uri = 'gmail+ssl://tttttttttttttt7%40gmail.com:oauth2@imap.gmail.com?archive=Archived'

class Mail(Message):
	pass