'''
    from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
    from django.utils import timezone
    import requests,sys, datetime
    from decimal import Decimal
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
    from django.contrib.auth import authenticate, login, logout
    from django.db.models import Sum, F
    import json
    import numpy as np
    #from .apps import cotacao_dolar
    from . import apps
    #o ponto antes de models se refere ao app/pasta atual (não precisa usar o .py)
'''

from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib.auth.decorators import  login_required
from datetime import date,datetime

@login_required
def Index(request):
    hoje = date.today()
    planos = Plano.objects.filter(
        inicio__lte=hoje,
        fim__gte=hoje, 
        usuario=request.user
        ) 
    #Entry.objects.filter(pub_date__range=(start_date, end_date))
    return render(request, 'treino/index.html',{
        'planos':planos,'usuario':request.user})

#================PLANO====================    

@login_required
def EditarPlano(request, pk=None):
    instancia = Plano()
    if pk:
        instancia = get_object_or_404(Plano, id=pk)
    else:
        instancia = Plano()
        instancia.usuario = request.user
    
    form = PlanoForm(
        request.POST or None, instance=instancia
        )
    #form.fields['treino'].queryset=Treino.objects.filter(usuario=request.user)
    if request.POST and form.is_valid():
        form.save()
        #data = instancia.data.strftime('%Y-%m-%d');
        return redirect('index')
    return render(request, 'treino/editarplano.html', {'form': form})
    
'''    
def nova_ordem(request):
    user = request.user
    consulta_empresas = Empresa.objects.all().values_list('codigo', flat=True)#tirar o flat pra receber uma tupla
    empresas = json.dumps(list(consulta_empresas))

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
                ativo.quantidade = ativo.quantidade + ordem.quantidade
            else:
                ativo.quantidade = quantidade_antiga - ordem.quantidade
            ativo.save()
            ordem.save()
            return redirect('ordem_detalhe', pk=ordem.pk)
    else:
        form = OrdemForm(user=request.user)
    return render(request, 'investe/ordem/edita_ordem.html',{'form':form,'empresas':empresas})



@login_required
def novo_tipo(request, id=None):
    instancia = Tipo()
    if id:
        instancia = get_object_or_404(Tipo, pk=id)
    else:
        instancia = Tipo()
        instancia.usuario = request.user
    
    form = TipoForm(request.POST or None, instance=instancia)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('novo_evento'))
    return render(request, 'eventos/novo_tipo.html', {'form': form})

@login_required
def deleta_plano(request, pk):
    ordem = get_object_or_404(Ordem, pk=pk)
    ordem.delete()
    return redirect('index')

@login_required
def edita_plano(request, pk):
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
     '''