from django.conf.urls import url
from django.urls import path, include
from . import views,admin

#from django.contrib import admin
#from django.views.generic import TemplateView

urlpatterns = [
    path('', views.EventosDiarios, name='eventos_diarios'),
    url(r'^calendario/$', views.Calendario.as_view(), name='calendario'),
    url(r'^eventos/novo/$', views.editar, name='novo_evento'),
    url(r'^eventos/editar/(?P<id>\d+)/$', views.editar, name='editar'),
    url(r'^eventos/novo_tipo/$', views.novo_tipo, name='novo_tipo'),
    url(r'^eventos/feito$', views.evento_feito, name='evento_feito'),
    url(r'^eventos/deletar/(?P<id>\d+)/$', views.deleta_evento, name='deleta_evento'),
]