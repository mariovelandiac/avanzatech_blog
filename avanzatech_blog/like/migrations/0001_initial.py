# Generated by Django 5.0.1 on 2024-01-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'resource is active'), ('inactive', 'resource is not active')], default='active', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]