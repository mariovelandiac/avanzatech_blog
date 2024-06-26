# Generated by Django 5.0.1 on 2024-01-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('read_permission', models.CharField(choices=[('public', 'Public: Anyone can access the post'), ('authenticated', 'Authenticated: any authenticated user can access the post'), ('team', 'Team: Any user on the same team as the post author can access the post'), ('author', 'Author: Only the author can access the post')], default='public', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
