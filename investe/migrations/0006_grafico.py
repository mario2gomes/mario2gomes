# Generated by Django 3.1.3 on 2020-12-19 16:31

from django.db import migrations, models
import django_matplotlib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('investe', '0005_auto_20200723_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grafico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('figura', django_matplotlib.fields.MatplotlibFigureField()),
            ],
        ),
    ]
