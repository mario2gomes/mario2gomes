# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from django.urls import reverse

class Evento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    inicio = models.TimeField()
    fim = models.TimeField()
    tipo = models.ForeignKey('Tipo', on_delete=models.DO_NOTHING)
    feito = models.BooleanField()
    observacao = models.TextField(blank=True,null=True)
    prioridade = models.CharField(choices=(('alta', 'alta'),('media', 'media'),('baixa', 'baixa')),max_length=10,null=False,default='baixa')
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap
 
    #pega a url da p�gina admin do model ??? n�o sei como nem pra qu� ???
    
    #pega a url da p�gina usada em admin
    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return '<a href="%s">%s</a>' % (url, str(self.descricao+'<br>'))
    
    #pega a url da p�gina usada em view
    @property
    def get_html_url(self):
        url = reverse('editar',args=[self.id])
        tag = 's' if self.feito else 'b'
        observacao = '...' if self.observacao else ''
        return f'<{tag}><a href="{url}" rel="popover" title="{self.observacao}"> {self.descricao}{observacao} </a></{tag}>'

    @property
    def get_deletar_url(self):
        url = reverse('deleta_evento',args=[self.id])
        alerta_deletar = "return confirm('Tem certeza que deseja deletar esse evento?');"
        icone_deletar = "class='fa fa-trash' data-toggle='tooltip' data-placement='bottom' style='color:#FF0000;'"
        return f'<a href="{url}" onclick="{alerta_deletar}"> <i {icone_deletar}></i> </a>'

    def clean(self):
        if self.fim <= self.inicio:
            raise ValidationError('O fim do evente n�o pode preceder seu in�cio')
 
        eventos = Evento.objects.filter(data=self.data, usuario=self.usuario)#substituir 2 pelo usuario logado
        if eventos.exists():
            for evento in eventos:
                if self.pk!=evento.pk and self.check_overlap(evento.inicio, evento.fim, self.inicio, self.fim):
                    raise ValidationError(
                        'Houve um choque de hor�rio com outro evento na mesma data: ' +evento.descricao+' ('+ str(evento.data) + ', ' + str(
                            evento.inicio) + '-' + str(evento.fim) + ')')

    def __str__(self):
        return self.descricao
    '''
    #customiza nome do model que aparece em admin
    class Meta:
        verbose_name = 'Scheduling'
        verbose_name_plural = 'Scheduling'
    '''

class Tipo(models.Model):
    descricao = models.CharField(max_length=20)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)


    def __str__(self):
    	return self.descricao