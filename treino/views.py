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

from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import  login_required
from datetime import date,datetime

@login_required
def index(request):
    hoje = date.today()
    plano = Plano.objects.filter(inicio<=hoje, fim >=hoje, usuario=request.user).order_by('-data')
    ativos = Ativo.objects.all().filter(usuario=usuario_logado).order_by('empresa')
    #grafico = Grafico.objects.filter(pk=1)
    empresas = []
    for ativo in ativos:
        empresa = get_object_or_404(Empresa, pk=ativo.empresa.pk)
        empresas.append(empresa)

    #lucro_nao_realizado_total, lucro_nao_realizado = Empresa.lucro_nao_realizado_total(usuario_logado)

    #totais = Ativo.objects.filter(usuario=usuario_logado).aggregate(lucro = Sum('lucro'),preco = Sum('preco'))
    return render(request, 'investe/index.html',{'ordens':ordens,'ativos':ativos,'empresas':empresas})#, 'totais':totais, 'lucro_nao_realizado':lucro_nao_realizado, 'lucro_nao_realizado_total':lucro_nao_realizado_total, 'grafico':grafico})