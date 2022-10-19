# Generated by Django 4.1.2 on 2022-10-19 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_legal_options_alter_natural_options_and_more'),
        ('investments', '0002_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='legal_profile',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='natural_profile',
        ),
        migrations.AddField(
            model_name='subscription',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='accounts.profile'),
            preserve_default=False,
        ),
    ]