# Generated by Django 5.0.1 on 2024-01-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_rename_modified_at_post_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_permission',
            field=models.CharField(choices=[('public', 'Public: Anyone can access the post'), ('authenticated', 'Authenticated: any authenticated user can access the post'), ('team', 'Team: Any user on the same team as the post author can access the post'), ('author', 'Author: Only the author can access the post')], default='public', max_length=20),
        ),
    ]
