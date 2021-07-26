import requests
from django import forms
from django.forms import ModelForm
from .models import *

class DespesaForm(ModelForm):
  class Meta:
    model = Despesa
    fields = ('nome', 'estabelecimento', 'valor', 'vencimento', 'data_pagamento', 'tipo', 'pagamento', 'parcelado')

class EstabelecimentoForm(ModelForm):
  class Meta:
    model = Estabelecimento
    fields = ('nome', 'tipo', 'endereco', 'cidade')

class FeiraForm(ModelForm):
  class Meta:
    model = Feira
    fields = ('data', 'supermercado', 'preco_total')

class ItemForm(ModelForm):
  class Meta:
    model = Item
    fields = ('nome', 'tipo', 'preco', 'quantidade', 'medida')