# Generated by Django 4.1.5 on 2023-02-28 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomObject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
    ]
