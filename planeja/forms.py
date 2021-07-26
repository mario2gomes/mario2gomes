import requests
from django import forms
from django.forms import ModelForm, DateInput, TimeInput
from .models import *

class EventoForm(ModelForm):

  def __init__(self, *args, **kws):
    self.usuario = kws.pop('user', None)
    super(EventoForm, self).__init__(*args, **kws)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['data'].input_formats = ('%Y-%m-%d',)
    self.fields['inicio'].input_formats = ('%H:%M',)
    self.fields['fim'].input_formats = ('%H:%M',)    
  
  class Meta:
    model = Evento
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'data': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
      'inicio': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
      'fim': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
    }    
    #tipo = forms.ModelChoiceField(queryset=(Tipo.objects.filter(usuario=request.user).values_list('descricao',flat=True)),to_field_name='descricao')
    fields = ('descricao','data','inicio','fim','feito','observacao','prioridade','tipo')


  
class TipoForm(ModelForm):
  class Meta:
    model = Tipo
    fields = ('descricao',)

  def __init__(self, *args, **kws):
      # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
      self.usuario = kws.pop('user', None)
      super(TipoForm, self).__init__(*args, **kws)