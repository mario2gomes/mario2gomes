# Generated by Django 3.1.4 on 2021-03-17 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treino', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treino_exercicio',
            old_name='repetições',
            new_name='repeticoes',
        ),
    ]
