from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
from datetime import timedelta
import datetime
from .models import Evento

#usado em views
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    #formata um dia como um td
    # filtra eventos por dia        
    def formatday(self, day, events):
        events_per_day = events.filter(data__day=day).order_by('inicio')
        d = ''
        for event in events_per_day:
            d += f'<li class="calendar_list"> {event.inicio.strftime("%H:%M")}-{event.fim.strftime("%H:%M")} {event.get_deletar_url} {event.get_html_url}</li>'
        
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    
    #formata a semana como um tr
    def formatweek(self, theweek, events,dias_semana):
        week = ''
        for d, weekday in theweek:
            week += dias_semana[weekday]+self.formatday(d, events)
        return f'<tr> {week} </tr>'

    #formata um mês como um table
    # filtra eventos por ano e mês    
    def formatmonth(self, withyear=True, usuario_logado=True):
        dias_semana = {0:'',1:'',2:'',3:'',4:'',5:'',6:''}
        events = Evento.objects.filter(data__year=self.year, data__month=self.month, usuario=usuario_logado)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, dias_semana)}\n'
        return cal





#usado em admin
class EventCalendar(HTMLCalendar):
    def __init__(self, eventos=None):
        super(EventCalendar, self).__init__()
        self.eventos = eventos
 
    def formatday(self, day, weekday, eventos):
        """
        Return a day as a table cell.
        """
        events_from_day = eventos.filter(data__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"
 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)
 
    def formatweek(self, theweek, eventos):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, eventos) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
 
        eventos = Evento.objects.filter(data__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, eventos))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)