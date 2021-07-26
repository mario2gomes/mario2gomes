from django.forms import ModelForm, DateInput
from datetime import date,datetime
import datetime, requests
from django import forms
from .models import Ordem, Ativo, Empresa, Usuario
from bs4 import BeautifulSoup

class OrdemForm(forms.ModelForm):
    #empresa = forms.ModelChoiceField(queryset=(Empresa.objects.all().values_list('codigo',flat=True)),to_field_name='codigo')
    # outra maneira de formatar a data: teste = forms.DateField(widget=DateInput)
    empresa = forms.CharField()
    quantidade = forms.DecimalField(min_value=0.00000009)
    preco = forms.DecimalField(min_value=0.01)
    moeda = forms.ChoiceField(choices=(('BRL', 'BRL'),('U$D', 'U$D')))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(OrdemForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['data'].input_formats = ('%Y-%m-%d',)

    class Meta:
        model = Ordem
        fields = ('tipo','data','quantidade','preco')
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {'data': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),}
        
    def clean_data(self):
        data = self.cleaned_data['data']
        if data > datetime.date.today():
            raise forms.ValidationError("Sua ordem não pode possuir data futura")
        return data

    def clean(self):
        cleaned_data=self.cleaned_data
        campo_moeda = cleaned_data.get('moeda')
        campo_tipo = cleaned_data.get('tipo')
        campo_empresa = cleaned_data.get('empresa').upper()
        campo_quantidade = cleaned_data.get('quantidade')
        empresa,criada = Empresa.objects.get_or_create(codigo=campo_empresa)

        if empresa.moeda and (campo_moeda != empresa.moeda):
                raise forms.ValidationError("A moeda informada não coincide com a moeda do seu ativo")
                
        preco = empresa.cotacao_atual()

        pagina = requests.get('https://br.advfn.com/bolsa-de-valores/bovespa/'+campo_empresa+'/cotacao')
        if pagina.status_code==200:
            if preco == 0:
                raise forms.ValidationError("Empresa sem valor estimado.")
            else:
                soup = BeautifulSoup(pagina.text, 'html.parser')
                tabelas = soup.find_all('div', class_ = "TableElement")
                nome = tabelas[0].find('table').find('tr', class_='odd').find_all('b')[0].get_text()
                bolsa = tabelas[0].find('table').find('tr', class_='odd').find_all('b')[2].get_text()
                tipo_ativo = tabelas[0].find('table').find('tr', class_='odd').find_all('span')[0].get_text()
                #moeda = tabelas[4].find('table').find('tr', class_='odd').find_all('td')[-1].get_text()

                #if len(moeda)!=3:
                #    moeda = 'U$D'

                Empresa.objects.filter(codigo=campo_empresa).update(nome=nome, 
                bolsa = bolsa, moeda = campo_moeda, tipo_ativo=tipo_ativo, preco=preco, data_preco=date.today())
        else:
            empresa.delete()
            raise forms.ValidationError("O código "+campo_empresa+" não existe na base de dados de ações")
        
        if campo_tipo == 'venda':
            try:
                novo_ativo = Ativo.objects.get(empresa=empresa.pk, usuario=self.user.pk)
            except Ativo.DoesNotExist:
                novo_ativo = False
            except:
                raise forms.ValidationError("O ativo existe mas houve um erro")
            if novo_ativo:
                quantidade_existente_ativo = novo_ativo.quantidade
                if campo_quantidade > quantidade_existente_ativo:
                    raise forms.ValidationError("A quantidade de venda é maior que a quantidade de ações que você possui")
            else:         
                raise forms.ValidationError("Você não tem ativos desta empresa para vender")
        return cleaned_data

field_empresa = OrdemForm.base_fields['empresa']
field_empresa.widget.attrs['id'] = 'myInput'
#field_data.widget.attrs["class"] = "datepicker"

#<input id="myInput">

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ()