import requests
from django import forms
from django.forms import ModelForm
from .models import *

class ItemForm(ModelForm):
  #em_estoque = forms.IntegerField()
  #empresa_id = forms.IntegerField()
  
  class Meta:
    model = Item
    fields = ('nome', 'descricao', 'preco', 'categoria', 'medida', 'unidade', 'observacao', 'imagem')

class EstabelecimentoForm(ModelForm):
  class Meta:
    model = Estabelecimento
    fields = ('nome','endereco','telefone','instagram','email','facebook','observacao')

  def __init__(self, *args, **kws):
    self.usuario = kws.pop('user', None)
    #super(ItemForm, self).__init__(*args, **kws)
    super(EstabelecimentoForm, self).__init__(*args, **kws)