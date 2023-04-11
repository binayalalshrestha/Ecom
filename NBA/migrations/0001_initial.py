# Generated by Django 4.1.5 on 2023-04-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('position', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('team', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
            ],
        ),
    ]
