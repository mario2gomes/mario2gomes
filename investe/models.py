from datetime import date,datetime
from django.db.models import Sum,Avg,Count,F,ExpressionWrapper,fields
from django.db.models.fields import DecimalField,IntegerField,DateTimeField
from django.conf import settings
from django.db import models
from django.utils import timezone
import requests, http.client, json, csv
from django.contrib.auth.models import User
from requests import get
from json import loads
from time import gmtime, mktime, strptime
from bs4 import BeautifulSoup
from decimal import Decimal
from django_matplotlib import MatplotlibFigureField

#Figuras de grÃ¡ficos
class Grafico(models.Model):
    figura = MatplotlibFigureField(figure='minha_figura')

#UsuÃ¡rio anÃ´nimo: django.contrib.auth.models.AnonymousUser
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=100)
    #exemplo de uso:
        #>>> u = User.objects.get(username='fsmith')
        #>>> fsmith_cep = u.usuario.cep

class Ordem(models.Model):    
    #ativo = models.ForeignKey('Ativo',on_delete=models.DO_NOTHING,null=True)
    empresa = models.ForeignKey('Empresa',on_delete=models.DO_NOTHING)
    tipo = models.CharField(choices=(('compra', 'compra'),('venda', 'venda')),max_length=10,null=False)
    preco = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    quantidade = models.DecimalField(max_digits=20,decimal_places=8,null=False)
    corretora = models.CharField(max_length=200, null=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    data = models.DateField(default=timezone.now, null=False)
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
    	#nome = '{}: {}'.format(self.empresa, self.data)
        return '{}: {}'.format(self.empresa, self.data)

class Ativo(models.Model):
    empresa = models.ForeignKey('Empresa',on_delete=models.DO_NOTHING,unique=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    #somado a cada compra e subtraido a cada venda
    #quantidade = soma de todas compras
    quantidade = models.DecimalField(max_digits=20,decimal_places=8,null=False,default=0)

    #a cada venda e a cada compra o preco medio Ã© atualizado
    #preÃ§o mÃ©dio das aÃ§oes ativas
    preco = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0)

    #somado a cada venda
    #lucro = quantidade_vendida * preco_venda - quantidade_vendida*preco_medio
    #lucro realizado
    lucro = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0)
    lucro_percentual = models.DecimalField(max_digits=10,decimal_places=4,null=False,default=0)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.empresa

    @property
    def lucro_diario(self):
        ordens = Ordem.objects.filter(empresa=self.empresa, tipo='compra', usuario=self.usuario)
        lucro_diario = 0
        for contador,ordem in enumerate(ordens):
            diferenca_dias = (date.today() - ordem.data).days
            lucro_diario = lucro_diario + (((
                ordem.empresa.preco - ordem.preco) / (
                    diferenca_dias if diferenca_dias > 0 else 1)) / (1 if ordem.preco == 0 else ordem.preco))
        lucro_diario = lucro_diario/(contador + 1)
        return lucro_diario
    
class Empresa(models.Model):
    nome = models.CharField(null=False,max_length=100)
    codigo = models.CharField(null=False, max_length=100, unique=True)
    preco = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    data_preco = models.DateField(null=True)
    segmento = models.CharField(null=True, max_length=100)
    codigo_api_uol = models.IntegerField(null=True)
    tipo_ativo = models.CharField(null=True, max_length=20)
    bolsa = models.CharField(null=True, max_length=100)
    moeda = models.CharField(null=True, max_length=10)
    
    def __str__(self):
        return self.nome
    #CotaÃ§Ã£o via web scrapping

    def lucro_nao_realizado_total(usuario_logado):
        #ordens = Ordem.objects.filter(usuario=request.user).order_by('-data')
        ativos = Ativo.objects.all().filter(usuario=usuario_logado).order_by('empresa')
        empresas = []
        for ativo in ativos:
            empresa = Empresa.objects.get(pk=ativo.empresa.pk)
            empresas.append(empresa)           

        #esse_ano = date.today().year
        lucro_nao_realizado = {}
        for ativo in ativos:
            if ativo.empresa.moeda != 'BRL':
                cambio = Decimal(Empresa.cotacao_dolar())
            else:
                cambio = 1

            lucro = cambio*ativo.quantidade*(ativo.empresa.preco - ativo.preco)
            lucro_nao_realizado[ativo.empresa.codigo] = lucro
        
        lucro_nao_realizado_total = sum(lucro_nao_realizado.values())
        #totais = Ativo.objects.filter(usuario=request.user).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
        return lucro_nao_realizado_total, lucro_nao_realizado

    def lucro_nao_realizado(self,usuario_logado):
        ativo = Ativo.objects.get(usuario=usuario_logado, pk=self.pk)
        if ativo.empresa.moeda != 'BRL':
            cambio = Decimal(Empresa.cotacao_dolar())
        else:
            cambio = 1

        lucro_nao_realizado = cambio*ativo.quantidade*(ativo.empresa.preco - ativo.preco)
        
        #totais = Ativo.objects.filter(usuario=request.user).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
        return lucro_nao_realizado

    def lucro_nao_realizado_anual(self):
        ordens = Ordem.objects.filter(usuario=request.user).order_by('-data')
        ativos = Ativo.objects.all().filter(usuario=request.user).order_by('empresa')
        empresas = []
        for ativo in ativos:
            empresa = get_object_or_404(Empresa, pk=ativo.empresa.pk)
            empresas.append(empresa)           

        esse_ano = date.today().year
        lucro_nao_realizado = {}
        for ativo in ativos:
            if ativo.empresa.moeda != 'BRL':
                cambio = Decimal(Empresa.cotacao_dolar())
            else:
                cambio = 1

            lucro = cambio*ativo.quantidade*(ativo.empresa.preco - ativo.preco)
            lucro_nao_realizado[ativo.empresa.codigo] = lucro
        
        lucro_nao_realizado_total = sum(lucro_nao_realizado.values())

        totais = Ativo.objects.filter(usuario=request.user).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
        return render(request, 'investe/index.html',{'ordens':ordens,'ativos':ativos,'empresas':empresas, 'totais':totais, 'lucro_nao_realizado':lucro_nao_realizado, 'lucro_nao_realizado_total':lucro_nao_realizado_total})

    def cotacao_atual(self):
        pagina_cotacao = requests.get('https://br.advfn.com/bolsa-de-valores/bovespa/'+self.codigo+'/cotacao')
        soup = BeautifulSoup(pagina_cotacao.text, 'html.parser')
        cota_busca = soup.find('span', class_ = "qs-current-price")
        cota = cota_busca.get_text()
        try:
            cotacao = Decimal(cota.replace('.','').replace(',','.'))
        except:
            return 'https://api.telegram.org/bot1454648470:AAFqV5megHg623GkVNSdOIdwGmWAupy32rY/sendMessage?chat_id=915928341&text=Erro na cotaÃ§Ã£o da empresa: '+self.codigo
        return cotacao

    def cotacao_dolar():
        empresa = Empresa.objects.get(codigo='USDBRL')
        valor_dolar = empresa.preco
        return valor_dolar