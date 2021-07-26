# Generated by Django 3.2.5 on 2021-07-14 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orcamento', '0002_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vencimento', models.IntegerField()),
                ('data_pagamento', models.DateTimeField()),
                ('parcelado', models.IntegerField(default=0)),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'despesa',
                'verbose_name_plural': 'despesas',
            },
        ),
        migrations.CreateModel(
            name='Estabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('tipo', models.CharField(choices=[('F', 'fisico'), ('I', 'internet')], max_length=8)),
                ('endereco', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=50)),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'estabelecimento',
                'verbose_name_plural': 'estabelecimentos',
            },
        ),
        migrations.CreateModel(
            name='Feira',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('preco_total', models.DecimalField(decimal_places=2, max_digits=4)),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('supermercado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.estabelecimento')),
            ],
            options={
                'verbose_name': 'feira',
                'verbose_name_plural': 'feiras',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=4)),
                ('quantidade', models.IntegerField()),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Medida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'medida',
                'verbose_name_plural': 'medidas',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('tipo', models.CharField(choices=[('C', 'CrÃ©dito'), ('D', 'DÃ©bito'), ('V', 'Ã\x80 Vista')], max_length=50)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'verbose_name': 'pagamento',
                'verbose_name_plural': 'pagamentos',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'tipo',
                'verbose_name_plural': 'tipos',
            },
        ),
        migrations.CreateModel(
            name='Tipo_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'tipo_item',
                'verbose_name_plural': 'tipo_items',
            },
        ),
        migrations.DeleteModel(
            name='Conta',
        ),
        migrations.DeleteModel(
            name='usuario',
        ),
        migrations.AddField(
            model_name='item',
            name='medida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.medida'),
        ),
        migrations.AddField(
            model_name='item',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.tipo_item'),
        ),
        migrations.AddField(
            model_name='despesa',
            name='estabelecimento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.estabelecimento'),
        ),
        migrations.AddField(
            model_name='despesa',
            name='pagamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.pagamento'),
        ),
        migrations.AddField(
            model_name='despesa',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orcamento.tipo'),
        ),
        migrations.AddField(
            model_name='despesa',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
