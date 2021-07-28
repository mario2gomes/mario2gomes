#from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

#from django.contrib import admin

urlpatterns = [
    path('', views.Index, name='index'),
    path('novoplano', views.EditarPlano, name='novoplano'),
    path('editarplano/<int:pk>', views.EditarPlano, name='editarplano'),
    #url(r'^editarplano/(?P<pk>\d+)/$', views.EditarPlano, name='editarplano'),
    #path('item/deletar/<pk>', views.DeletarItem, name='deletar_item')
]