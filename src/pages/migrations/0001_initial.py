# Generated by Django 3.0.4 on 2020-03-31 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_mailbox', '0008_auto_20190219_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_mailbox.Message')),
            ],
            bases=('django_mailbox.message',),
        ),
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('mailbox_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_mailbox.Mailbox')),
            ],
            bases=('django_mailbox.mailbox',),
        ),
    ]
