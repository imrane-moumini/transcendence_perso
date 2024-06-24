# Generated by Django 5.0.6 on 2024-06-24 21:04

import pong.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0003_newuser_is_mfa_enabled_newuser_mfa_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', validators=[pong.models.validate_image]),
        ),
    ]
