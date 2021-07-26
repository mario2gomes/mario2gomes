from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('clearcache/', include('clearcache.urls')),
    path('usuario/cadastrar_usuario', views.cadastrar_usuario, name="cadastrar_usuario"),
    #path('endereço url', views.função na view, name='nome que aparece no chamador desse link')
    path('', views.index, name='index'),
    path('atualiza_preco/', views.atualiza_preco, name='atualiza_preco'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    #path('', TemplateView.as_view(template_name="investe/index.html")),
    #path('', TemplateView.as_view(index="index.html")),
    #path('ordem/lista/', views.ordem_lista, name='ordem_lista'),
    path('ordem/<int:pk>/', views.ordem_detalhe, name='ordem_detalhe'),
    path('ordem/nova/', views.nova_ordem, name='nova_ordem'),
    path('ordem/<int:pk>/editar/', views.edita_ordem, name='edita_ordem'),
    path('ordem/<pk>/deletar/', views.deleta_ordem, name='deleta_ordem'),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ATIVO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #path('ativo/lista/', views.ativo_lista, name='ativo_lista'),
    path('ativo/<int:pk>/', views.ativo_detalhe, name='ativo_detalhe'),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EMPRESA<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #path('empresa/lista/', views.empresa_lista, name='empresa_lista'),
    path('empresa/<int:pk>/', views.empresa_detalhe, name='empresa_detalhe'),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>USUARIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    path('usuario/lista/', views.usuario_lista, name='usuario_lista'),
    path('usuario/<int:pk>/', views.usuario_detalhe, name='usuario_detalhe'),
    path('usuario/<int:pk>/editar/', views.edita_usuario, name='edita_usuario'),
    path('usuario/<pk>/deletar/', views.deleta_usuario, name='deleta_usuario'),
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TESTE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    path('teste', views.teste,name = 'teste'),
    ]