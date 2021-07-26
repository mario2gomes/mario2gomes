import requests
from django import forms
from django.forms import ModelForm
from .models import *

class PlanoForm(ModelForm):
  class Meta:
    model = Plano
    fields = ('nome', 'descricao', 'inicio', 'fim')

class TreinoForm(ModelForm):
  class Meta:
    model = Treino
    fields = ('nome', 'descricao', 'data')

class Treino_exercicioForm(ModelForm):
  class Meta:
    model = Treino_exercicio
    fields = ('treino', 'exercicio', 'carga', 'repeticoes', 'medida')

class ExercicioForm(ModelForm):
  class Meta:
    model = Exercicio
    fields = ('nome', 'descricao', 'grupo_muscular', 'imagem')