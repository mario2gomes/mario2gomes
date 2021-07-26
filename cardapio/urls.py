from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

#from django.contrib import admin

urlpatterns = [
    path('index', views.Index, name='index'),
    path('cliente/<pk>', views.CardapioCliente, name='cardapio_cliente'),
    path('', views.Estabelecimentos, name='estabelecimentos'),
    path('estabelecimento/cardapio/<pk>', views.CardapioEstabelecimento, name='cardapio_estabelecimento'),
    path('estabelecimento/novo', views.EditarEstabelecimento, name='novo_estabelecimento'),
    path('estabelecimento/editar/<pk>', views.EditarEstabelecimento, name='editar_estabelecimento'),
    path('estabelecimento/deletar/<pk>', views.DeletarEstabelecimento, name='deletar_estabelecimento'),
    path('item/novo/<pk_estabelecimento>', views.EditarItem, name='novo_item'),
    path('item/editar/<pk>', views.EditarItem, name='editar_item'),
    path('item/deletar/<pk>', views.DeletarItem, name='deletar_item'),
    path('item/falta', views.FaltaItem, name='falta_item'),
    #url(r'^item/falta$', views.FaltaItem, name='falta_item'),
]