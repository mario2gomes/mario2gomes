import requests
from django import forms
from django.forms import ModelForm
from .models import *

class ViagemForm(ModelForm):      
  class Meta:
    model = Viagem
    fields = ('nome', 'usuario', 'inicio', 'fim')

class GastoForm(ModelForm):      
  class Meta:
    model = Gasto
    fields = ('tipo_gasto', 'valor', 'data_pagamento', 'moeda')

class TransporteForm(ModelForm):      
  class Meta:
    model = Transporte
    fields = ('nome', 'observacao', 'data_saida', 'data_chegada', 'local_saida', 'local_chegada')

class HospedagemForm(ModelForm):      
  class Meta:
    model = Hospedagem
    fields = ('nome','observacao', 'endereco', 'checkin', 'checkout')

class RoteiroForm(ModelForm):      
  class Meta:
    model = Roteiro
    fields = ('nome')

class AtracaoForm(ModelForm):      
  class Meta:
    model = Atracao
    fields = ('data', 'observacao', 'endereco', 'cidade', 'estado', 'pais')


class ItemForm(ModelForm):      
  class Meta:
    model = Item
    fields = ('nome', 'peso', 'tipo_item', 'observacao', 'inicio', 'fim')

class Tipo_itemForm(ModelForm):      
  class Meta:
    model = Tipo_item
    fields = ('nome')

class FotoForm(ModelForm):      
  class Meta:
    model = Foto
    fields = ('nome', 'imagem', 'data')