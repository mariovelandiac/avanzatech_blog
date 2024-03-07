# Generated by Django 5.0.1 on 2024-03-06 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_alter_postcategorypermission_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategorypermission',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_category_permissions', to='post.post'),
        ),
    ]
