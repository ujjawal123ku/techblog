# Generated by Django 4.2.11 on 2024-04-08 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]