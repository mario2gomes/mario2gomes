from datetime import date,datetime
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.utils import timezone
from .models import Ordem, Ativo, Empresa, Usuario, User, Grafico
from .forms import OrdemForm
from django.contrib.auth.decorators import  login_required
import requests,sys, datetime
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, F
import json
import numpy as np
#from .apps import cotacao_dolar
#from . import apps
#o ponto antes de models se refere ao app/pasta atual (não precisa usar o .py)

def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('index')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'investe/usuario/cadastrar_usuario.html', {'form_usuario': form_usuario})

def atualiza_preco(request):   
    empresas = Empresa.objects.all()

    for empresa in empresas:
        cotacao_atual = empresa.cotacao_atual()
        if type(cotacao_atual) == str:
            return redirect(cotacao_atual)
        else:
            Empresa.objects.filter(pk=empresa.pk).update(preco=cotacao_atual)
        Empresa.objects.filter(pk=empresa.pk).update(data_preco=date.today())
    valor_dolar = Empresa.cotacao_dolar()
    if float(valor_dolar) < 5 or float(valor_dolar)>5.5:
        return redirect('https://api.telegram.org/bot1454648470:AAFqV5megHg623GkVNSdOIdwGmWAupy32rY/sendMessage?chat_id=915928341&text=Preço do dolar hoje: R$ '+str(valor_dolar))
    return render(request,'investe/atualiza_preco.html', {'valor_dolar': valor_dolar})  

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ORDEM<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@login_required
def index(request):
    request.session['alerta'] = 0
    usuario_logado = request.user
    ordens = Ordem.objects.filter(usuario=usuario_logado).order_by('-data')
    ativos = Ativo.objects.all().filter(usuario=usuario_logado).order_by('empresa')
    #grafico = Grafico.objects.filter(pk=1)
    empresas = []
    for ativo in ativos:
        empresa = get_object_or_404(Empresa, pk=ativo.empresa.pk)
        empresas.append(empresa)
    valor_dolar = Empresa.cotacao_dolar()
    #lucro_nao_realizado_total, lucro_nao_realizado = Empresa.lucro_nao_realizado_total(usuario_logado)
    #totais = Ativo.objects.filter(usuario=usuario_logado).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
    
    #informações para o modal de nova ordem
    #user = request.user
    consulta_empresas = Empresa.objects.all().values_list('codigo', flat=True)#tirar o flat pra receber uma tupla
    todas_empresas = json.dumps(list(consulta_empresas))
    form = OrdemForm(user=request.user)
    return render(
        request, 'investe/index.html',{
            'ordens':ordens,
            'ativos':ativos,
            'empresas':empresas,
            'valor_dolar':valor_dolar,
            'form':form,
            'todas_empresas':todas_empresas
            })#, 'totais':totais, 'lucro_nao_realizado':lucro_nao_realizado, 'lucro_nao_realizado_total':lucro_nao_realizado_total, 'grafico':grafico})

@login_required
def estatisticas(request):
    #request.session['alerta'] = 0
    usuario_logado = request.user
    ativos = Ativo.objects.all().filter(usuario=usuario_logado)
    ordens = Ordem.objects.all().filter(usuario=usuario_logado)
    empresas = Empresa.objects.all()
    grafico = Grafico.objects.filter(pk=1)

    valor_dolar = empresas[0].preco
    lucro_nao_realizado_total, lucro_nao_realizado = Empresa.lucro_nao_realizado_total(usuario_logado)

    lucro_totais = Ativo.objects.filter(usuario=usuario_logado).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
    total_investido = 0
    for ordem in ordens:
        if ordem.empresa.moeda == 'U$D':
            ordem.preco = ordem.preco*empresas[0].preco

        if ordem.tipo == 'compra':
            total_investido = total_investido + (ordem.preco * ordem.quantidade)
        else:
            total_investido = total_investido - (ordem.preco * ordem.quantidade)

    total_atual = 0
    for ativo in ativos:

        if ativo.empresa.moeda == 'U$D':
            ativo.empresa.preco = ativo.empresa.preco*empresas[0].preco

        total_atual = total_atual + (ativo.empresa.preco*ativo.quantidade)
    total_atual = total_atual - (lucro_totais['lucro'] if isinstance(lucro_totais['lucro'], Decimal) else 0)

    return render(request, 'investe/estatisticas.html',{'lucro_totais':lucro_totais, 'lucro_nao_realizado':lucro_nao_realizado, 'lucro_nao_realizado_total':lucro_nao_realizado_total, 'grafico':grafico, 'total_investido':total_investido, 'total_atual':total_atual, 'valor_dolar':valor_dolar})

@login_required
def ordem_detalhe(request, pk):
    ordem = get_object_or_404(Ordem, pk=pk)    
    #ordem.objects.get(pk=pk)
    return render(request, 'investe/ordem/ordem_detalhe.html',{'ordem':ordem})

@login_required
def nova_ordem(request):
    user = request.user
    if request.method == "POST":
        form = OrdemForm(request.POST,user=request.user)
        if form.is_valid():
            ordem = form.save(commit=False)
            empresa = get_object_or_404(Empresa, codigo=request.POST['empresa'].upper())
            ordem.empresa = empresa
            ordem.usuario = user
            ativo,criado = Ativo.objects.update_or_create(
                empresa=empresa, usuario = user)
            if ordem.tipo=='compra':
                ativo.preco = ((ativo.preco * ativo.quantidade) + (ordem.preco * ordem.quantidade)) / (ativo.quantidade + ordem.quantidade)
                ativo.quantidade = ativo.quantidade + ordem.quantidade
            else:
                lucro_antigo = ativo.lucro
                quantidade_antiga = ativo.quantidade
                lucro_percentual_antigo = ativo.lucro_percentual
                ativo.quantidade = quantidade_antiga - ordem.quantidade
                ativo.lucro = lucro_antigo + (ordem.preco * ordem.quantidade) - (ativo.preco * ordem.quantidade)
                ativo.lucro_percentual = ativo.lucro / ((lucro_antigo / (1 if lucro_percentual_antigo==0 else lucro_percentual_antigo)) + (ativo.preco * ordem.quantidade))
            ativo.save()
            ordem.save()
            return redirect('ordem_detalhe', pk=ordem.pk)
    else:
        form = OrdemForm(user=request.user)
    return render(request, 'investe/ordem/nova_ordem.html',{'form':form})

@login_required
def deleta_ordem(request, pk):
    #obtem ordem do banco pela pk
    ordem = get_object_or_404(Ordem, pk=pk)
    #Apenas a última ordem (da empresa) pode ser deletada (para facilitar o cálculo do lucro)
    if ordem == Ordem.objects.filter(empresa=ordem.empresa, usuario=request.user).last():
        ativo = Ativo.objects.get(empresa=ordem.empresa, usuario=request.user)
        if ordem.tipo=='compra':
            ativo.preco = ((ativo.preco * ativo.quantidade) - (ordem.preco * ordem.quantidade)) / (1 if ativo.quantidade == ordem.quantidade else ativo.quantidade - ordem.quantidade)
            ativo.quantidade = ativo.quantidade - ordem.quantidade
        else:
            lucro_antigo = ativo.lucro
            quantidade_antiga = ativo.quantidade
            lucro_percentual_antigo = ativo.lucro_percentual
            ativo.quantidade = quantidade_antiga + ordem.quantidade
            ativo.lucro = lucro_antigo - (ordem.preco * ordem.quantidade) + (ativo.preco * ordem.quantidade)
            y = lucro_percentual_antigo
            x = (lucro_antigo / (1 if y ==0 else y)) - (ativo.preco * ordem.quantidade)
            ativo.lucro_percentual = ativo.lucro / (1 if x==0 else x)
        ativo.save()
        ordem.delete()
        if ativo.quantidade == 0:
            ativo.delete()
        request.session['alerta'] = 'sem-erro'
    else:
        #deve enviar um alerta informando que apenas a última ordem pode ser deletada
        return redirect('index')
    
    return redirect('index')

@login_required
def edita_ordem(request, pk):
     ordem = get_object_or_404(Ordem, pk=pk)
     if request.method == "POST":
         form = OrdemForm(request.POST, instance=ordem)
         if form.is_valid():
             ordem = form.save(commit=False)
             ordem.save()
             return redirect('ordem_detalhe', pk=ordem.pk)
     else:
         form = OrdemForm(instance=ordem)
     return render(request, 'investe/ordem/edita_ordem.html', {'form': form})
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>ATIVO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@login_required
def ativo_detalhe(request, pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    return render(request, 'investe/ativo/ativo_detalhe.html',{'ativo':ativo})

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>EMPRESA<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def empresa_detalhe(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    return render(request, 'investe/empresa/empresa_detalhe.html',{'empresa':empresa})

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>USUARIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@login_required
def usuario_lista(request):
    usuarios = Usuario.objects.order_by('id')
    return render(request, 'investe/usuario/usuario_lista.html',{'usuarios':usuarios})

@login_required
def usuario_detalhe(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'investe/usuario/usuario_detalhe.html',{'usuario':usuario})

@login_required
def edita_usuario(request, pk):
     usuario = get_object_or_404(Usuario, pk=pk)
     if request.method == "POST":
         form = UsuarioForm(request.POST, instance=usuario)
         if form.is_valid():
             usuario = form.save(commit=False)
             usuario.save()
             return redirect('usuario_detalhe', pk=usuario.pk)
     else:
         form = UsuarioForm(instance=usuario)
     return render(request, 'investe/usuario/edita_ativo.html', {'form': form})

@login_required
def deleta_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.delete()
    return redirect('usuario_lista')

def teste(request):
    return render(request, 'investe/teste.html')