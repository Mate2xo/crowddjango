# Generated by Django 4.1.2 on 2022-10-13 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_legal_legalprofile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturalprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='naturalprofile',
            name='last_name',
        ),
    ]
