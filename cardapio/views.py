'''
from datetime import date,datetime, timedelta
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import json
'''
from django.urls import reverse#, reverse_lazy
#from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from cardapio.models import Estabelecimento,Item,Categoria,Medida 
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

@staff_member_required
def Index(request):
    return render(request, 'index.html')

def Estabelecimentos(request):
    if request.user.is_staff:
        estabelecimentos =Estabelecimento.objects.all()
    else:
        estabelecimentos = Estabelecimento.objects.filter(usuario=request.user)
    return render(request, 'estabelecimento/estabelecimentos.html', {'estabelecimentos': estabelecimentos})

@login_required
def CardapioEstabelecimento(request, pk=None):
    if(request.user.is_staff):
        estabelecimento = Estabelecimento.objects.get(id=pk)
    else:
        estabelecimento, criado = Estabelecimento.objects.get_or_create(usuario=request.user)
    itens = Item.objects.filter(estabelecimento=estabelecimento)

    #return HttpResponseRedirect(reverse('cardapio_estabelecimento'))
    return render(request, 'estabelecimento/cardapio_estabelecimento.html', {'itens': itens, 'estabelecimento':estabelecimento})


@login_required
def EditarEstabelecimento(request, pk=None):
    instancia = Estabelecimento()
    if pk:
        instancia = get_object_or_404(Estabelecimento, pk=pk)
        if instancia.usuario != request.user:
            html = "<html><body><h1>Apenas o proprietário deste estabelecimento tem permissão de alterá-lo</h></body></html>"
            return HttpResponse(html)
    else:
        instancia.usuario = request.user
    
    form = EstabelecimentoForm(request.POST or None, instance=instancia)
    if request.POST and form.is_valid():
        form.save()
        return redirect('cardapio_estabelecimento',pk=pk)

    return render(request, 'estabelecimento/novo_item.html', {'form': form})

def DeletarEstabelecimento(request, pk):
    #LEMBRAR DE DELETAR TODOS OS ITENS DESSE ESTABELECIMENTO
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    if estabelecimento.usuario != request.user:
        html = "<html><body><h1>Apenas o proprietário deste estabelecimento tem permissão de deletá-lo</h></body></html>"
        return HttpResponse(html)
    estabelecimento.delete()
    return redirect('/cardapio')

def CardapioCliente(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    itens = Item.objects.filter(estabelecimento=estabelecimento.pk)
    return render(request, 'cardapio/cardapio_cliente.html', {'itens': itens,'estabelecimento':estabelecimento})

@login_required
def EditarItem(request, pk=None, pk_estabelecimento=None):
    #periodo = self.request.GET.get('periodo', None)
    instancia = Item()

    if pk:
        instancia = get_object_or_404(Item, pk=pk)
        estabelecimento = Estabelecimento.objects.get(pk=instancia.estabelecimento.pk)
    else:
        estabelecimento = Estabelecimento.objects.get(pk=pk_estabelecimento)
        instancia.usuario = request.user
    
    if estabelecimento.usuario != request.user:
        html = "<html><body><h1>Apenas o proprietário deste estabelecimento tem permissão de alterá-lo</h></body></html>"
        return HttpResponse(html)

    form = ItemForm(request.POST or None, instance=instancia)
    form.fields['categoria'].queryset=Categoria.objects.filter(estabelecimento=estabelecimento)

    if request.POST and form.is_valid():
        item = form.save(commit=False)
        item.em_estoque = 1
        item.estabelecimento_id = estabelecimento.pk
        item.save()
        url = reverse('cardapio_estabelecimento', kwargs={'pk': instancia.estabelecimento.pk})
        return HttpResponseRedirect(url)
    return render(request, 'estabelecimento/novo_item.html', {'form': form})

@csrf_exempt
def FaltaItem(request):
    Item.objects.filter(id=request.POST.get('item')).update(em_estoque=request.POST.get('em_estoque'))
    data = {'message': "%s added" % request.POST.get('item')}
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def DeletarItem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.estabelecimento.usuario != request.user:
        html = "<html><body><h1>Apenas o proprietário deste estabelecimento tem permissão de alterá-lo</h></body></html>"
        return HttpResponse(html)
    item.delete()
    return redirect('cardapio_estabelecimento',pk=pk)

