# Generated by Django 4.1.5 on 2023-02-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_image_customer_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
