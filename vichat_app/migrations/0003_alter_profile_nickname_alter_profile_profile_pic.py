# Generated by Django 4.2 on 2023-04-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vichat_app', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.CharField(max_length=400),
        ),
    ]