# Generated by Django 4.1.2 on 2022-10-12 09:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Legal',
            new_name='LegalProfile',
        ),
        migrations.RenameModel(
            old_name='Natural',
            new_name='NaturalProfile',
        ),
    ]
