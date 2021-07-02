# Generated by Django 3.2.3 on 2021-06-21 15:29

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default=account.models.get_default_profile_image, max_length=255, null=True, upload_to='profile_images/'),
        ),
    ]