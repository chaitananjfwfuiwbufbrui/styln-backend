# Generated by Django 3.2.20 on 2023-08-15 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_slot',
            name='dateandtime',
            field=models.DateTimeField(),
        ),
    ]
