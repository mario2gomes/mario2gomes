# Generated by Django 3.1.3 on 2020-12-28 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('data', models.DateField()),
                ('inicio', models.TimeField()),
                ('fim', models.TimeField()),
                ('feito', models.BooleanField()),
                ('observacao', models.TextField(blank=True, null=True)),
                ('prioridade', models.CharField(choices=[('alta', 'alta'), ('media', 'media'), ('baixa', 'baixa')], default='baixa', max_length=10)),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('tipo_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planeja.tipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
