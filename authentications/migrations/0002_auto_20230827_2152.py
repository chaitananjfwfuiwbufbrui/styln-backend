# Generated by Django 3.2.20 on 2023-08-27 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='experiance',
            field=models.CharField(blank=True, default='1', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='role',
            field=models.CharField(blank=True, default='baber', max_length=50, null=True),
        ),
    ]
