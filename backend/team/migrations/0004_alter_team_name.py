# Generated by Django 5.0.1 on 2024-03-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_alter_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(default='Default Team', max_length=255, unique=True),
        ),
    ]
