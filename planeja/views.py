from django.shortcuts import render, get_object_or_404, redirect
from datetime import date,datetime, timedelta
from .models import *
from .forms import *
from .utils import Calendar
from django.http import HttpResponse, HttpResponseRedirect
#from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
import calendar
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import json

@login_required
def editar(request, id=None):
    instancia = Evento()
    if id:
        instancia = get_object_or_404(Evento, pk=id)
    else:
        instancia = Evento()
        instancia.usuario = request.user
    
    form = EventoForm(request.POST or None, instance=instancia)
    form.fields['tipo'].queryset=Tipo.objects.filter(usuario=request.user)
    if request.POST and form.is_valid():
        form.save()
        #return HttpResponseRedirect(reverse('eventos_diarios'))
        #return redirect(request.META['HTTP_REFERER'])
        data = instancia.data.strftime('%Y-%m-%d');
        return redirect('/planeja/calendario/?data_exibida='+data+'&periodo=semana')
    return render(request, 'eventos/editar.html', {'form': form})

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
def EventosDiarios(request):
    hoje = date.today()
    eventos = Evento.objects.filter(data=hoje,usuario=request.user).order_by('-data','inicio')
    return render(request, 'eventos/eventos_diarios.html', {'eventos': eventos,'hoje':hoje})

@csrf_exempt
def evento_feito(request):
    Evento.objects.filter(id=request.POST.get('item')).update(feito=request.POST.get('feito'))
    data = {'message': "%s added" % request.POST.get('item')}
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def deleta_evento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    evento.delete()    
    return redirect(request.META['HTTP_REFERER'])

class Calendario(LoginRequiredMixin, generic.ListView):
    model = Evento
    template_name = 'eventos/calendario.html'
    #success_url = reverse_lazy("calendar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #usa a data de hoje para o calendário e define o período a exibir (dia, mês ou semana)
        d = get_date(self.request.GET.get('data_exibida', None))
        periodo = self.request.GET.get('periodo', None)

        #instancia a classe calendario com a data e ano de hoje
        cal = Calendar(d.year, d.month)
        
        eventos = Evento.objects.filter(usuario=self.request.user).order_by('-data')#substituir 2 por usuario logado
        
        #chama o método formatmonth, que retorna nosso calendário como tabela
        html_cal_mensal = cal.formatmonth(withyear=True, usuario_logado=self.request.user)
        
        #para usar no método/página semanal
        dias_semana = {0:'seg: ',1:'ter: ',2:'qua: ',3:'qui: ',4:'sex: ',5:'sab: ',6:'dom'}
        ultimo_domingo = d - timedelta(d.weekday())
        week = [((ultimo_domingo + timedelta(dia)).day,dia) for dia in range(7)]
        eventos_semana = Evento.objects.filter(usuario=self.request.user, data__range=[ultimo_domingo, (ultimo_domingo + timedelta(6))]).order_by('-data')
        html_cal_semanal = cal.formatweek(week,eventos_semana,dias_semana)

        #para usar no método/página diário
        html_cal_diario = cal.formatday(d.day,eventos)
        
        if periodo == 'mes':
            tipo_calendario = html_cal_mensal
            context['anterior'] = prev_month(d)
            context['proximo'] = next_month(d)
        elif periodo == 'semana':
            tipo_calendario = html_cal_semanal
            context['anterior'] = prev_week(d)
            context['proximo'] = next_week(d)
        else:
            tipo_calendario = html_cal_diario
            context['anterior'] = prev_day(d)
            context['proximo'] = next_day(d)            

        context['calendar'] = mark_safe(tipo_calendario)
        context['periodo'] = 'periodo='+str(periodo)
        context['data_inicial'] = d
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    data_exibida = 'data_exibida=' + str(prev_month.year) + '-' + str(prev_month.month) + '-' + str(prev_month.day)
    return data_exibida

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    data_exibida = 'data_exibida=' + str(next_month.year) + '-' + str(next_month.month) + '-' + str(next_month.day)
    return data_exibida

def prev_week(d):
    prev_week = d - timedelta(days=7)
    data_exibida = 'data_exibida=' + str(prev_week.year) + '-' + str(prev_week.month)+ '-' + str(prev_week.day)
    return data_exibida

def next_week(d):
    next_week = d + timedelta(days=7)
    data_exibida = 'data_exibida=' + str(next_week.year) + '-' + str(next_week.month) + '-' + str(next_week.day)
    return data_exibida

def prev_day(d):
    prev_day = d - timedelta(days=1)
    data_exibida = 'data_exibida=' + str(prev_day.year) + '-' + str(prev_day.month)+ '-' + str(prev_day.day)
    return data_exibida

def next_day(d):
    next_day = d + timedelta(days=1)
    data_exibida = 'data_exibida=' + str(next_day.year) + '-' + str(next_day.month) + '-' + str(next_day.day)
    return data_exibida

def get_date(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return date.today()