# Generated by Django 5.0.1 on 2024-01-23 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 64 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=64, unique=True, verbose_name='username'),
        ),
    ]