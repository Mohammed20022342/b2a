# Generated by Django 5.0.7 on 2024-11-30 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone_verified',
            new_name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
    ]
