import requests
from django import forms
from django.forms import ModelForm
from .models import *

class PostagemForm(ModelForm):
  class Meta:
    model = Postagem
    fields = ('titulo', 'url', 'texto', 'categoria', 'publico', 'imagem')

class RespostaForm(ModelForm):
  class Meta:
    model = Resposta
    fields = ('texto')
    