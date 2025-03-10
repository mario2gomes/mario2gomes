from django.contrib import admin
from .models import Evento,Tipo
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento

class EventoAdmin(ImportExportModelAdmin):
    resource_class = EventoResource

admin.site.register(Evento, EventoAdmin)
admin.site.register(Tipo)
# inclusão de um calendário em eventos/admin

'''

# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from .utils import EventCalendar
 



class EventoAdmin(admin.ModelAdmin):
    list_display = ['data', 'inicio', 'fim', 'descricao']
    change_list_template = 'admin/eventos/change_list.html'

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}
 
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()
 
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month
 
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month
 
        extra_context['previous_month'] = 0#reverse('admin:eventos_evento_changelist') + '?day__gte=' + str(previous_month)
        extra_context['next_month'] = 0#reverse('admin:eventos_evento_changelist') + '?day__gte=' + str(next_month)
 
        #cal = HTMLCalendar()
        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventoAdmin, self).changelist_view(request, extra_context)
'''
