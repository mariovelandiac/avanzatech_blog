# Generated by Django 5.0.1 on 2024-03-05 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('permission', '0001_initial'),
        ('post', '0005_alter_post_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategoryPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.permission')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'unique_together': {('post', 'category', 'permission')},
            },
        ),
    ]
