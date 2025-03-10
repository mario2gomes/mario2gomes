# Generated by Django 3.1.4 on 2021-03-10 22:08

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
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('url', models.SlugField(max_length=20, unique=True)),
                ('texto', models.CharField(max_length=10000)),
                ('publico', models.IntegerField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('atualizacao', models.DateTimeField(auto_now=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.categoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'postagem',
                'verbose_name_plural': 'postagens',
            },
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=500)),
                ('publico', models.IntegerField()),
                ('criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('atualizacao', models.DateTimeField(auto_now=True, null=True)),
                ('postagem', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.postagem')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'resposta',
                'verbose_name_plural': 'respostas',
            },
        ),
    ]
