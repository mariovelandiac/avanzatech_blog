# Generated by Django 5.0.1 on 2024-03-08 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_postcategorypermission_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='read_permission',
        ),
        migrations.AlterField(
            model_name='postcategorypermission',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_category_permission', to='post.post'),
        ),
    ]