# Generated by Django 2.2.5 on 2020-07-23 22:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('investe', '0004_auto_20200723_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordem',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
