from django.utils import simplejson
from django import forms
from django.core.exceptions import ValidationError
from piston.handler import BaseHandler
from piston.utils import rc
from django.core import serializers
import json
import datetime
from dateutil.relativedelta import relativedelta
import time

from airports.models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight

class FlightHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = Flight
    
    @classmethod
    def resource_uri(cls, flight):
        return ('flight', ['json', ])

    def read(self, request, flight=None, month=None, day=None, ffrom=None, fto=None):
        base = Flight.objects
        filter_dict = {}
        flight_date = False
        if month and day:
            try:
                flight_date = datetime.date(year=datetime.datetime.now().year, month=int(month), day=int(day))
            except TypeError:
                return rc.BAD_REQUEST
        if flight:
            filter_dict['flight__iexact'] = flight
        if flight_date:
            filter_dict['datetime_scheduled__year'] = flight_date.year
            filter_dict['datetime_scheduled__month'] = flight_date.month
            filter_dict['datetime_scheduled__day'] = flight_date.day
        if ffrom and ffrom != 'all':
            filter_dict['city_of_departure__iexact'] = ffrom
        if fto and fto != 'all':
            filter_dict['city_of_arrival__iexact'] = fto
        if not filter_dict:
            start_date = datetime.datetime.now() + relativedelta(minutes=-30)
            end_date = datetime.datetime.now() + relativedelta(minutes=+30)
            filter_dict['datetime_scheduled__range'] = (start_date, end_date)
        flights = base.filter(**filter_dict).values()
        for flight in flights:
            flight['datetime_scheduled'] = flight['datetime_scheduled'].strftime("%a %b %d %Y %X")
            if flight['datetime_estimated']:
                flight['datetime_estimated'] = flight['datetime_estimated'].strftime("%a %b %d %Y %X")
            if flight['datetime_actual']:
                flight['datetime_actual'] = flight['datetime_actual'].strftime("%a %b %d %Y %X")
        return flights
#        if flight and flight_date:
#            if ffrom and fto:
#                return base.filter(datetime_scheduled__contains=flight_date.isoformat(), flight=flight, airport_of_departure=ffrom, airport_of_arrival=fto)
#            else:
#                return base.filter(datetime_scheduled__contains=flight_date.isoformat(), flight=flight)
#        else:
#            if flight_date and ffrom and fto:
#                return base.filter(datetime_scheduled__contains=flight_date.isoformat(), airport_of_departure=ffrom, airport_of_arrival=fto)
#            else:
#                return base.all()

    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        if 'data' in attrs:
            attrs = json.loads(request.POST.get('data'))
        else:
            return rc.BAD_REQUEST
#        for field in ('flight_status', 'comment', 'checkin_desk'):
#            attrs[field] = attrs[field] or u''
        try:
            inst = self.model.objects.get(**attrs)
            print 'Duplicate entry: %s' % inst
            #return rc.DUPLICATE_ENTRY
            return inst
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            inst = self.model(**attrs)
            try:
                inst.full_clean()
            except ValidationError, e:
                resp = rc.BAD_REQUEST
                resp.write(' ')
                resp.write(' '.join(["%s: %s;" % (k,v[0].rstrip('.')) for k,v in e.message_dict.items()]))
                return resp
            try:
                exinst = self.model.objects.get(flight=attrs['flight'], datetime_scheduled=attrs['datetime_scheduled'])
                exinst.flight_status = attrs['flight_status'] or u''
                exinst.datetime_estimated = attrs['datetime_estimated']
                exinst.datetime_actual = attrs['datetime_actual']
                exinst.save()
                return exinst
            except self.model.DoesNotExist:
                inst.save()
            #return serializers.serialize('json', [inst], ensure_ascii=False)
                return inst
        except Exception, e:
            print 'Error: %s' % e
            resp = rc.BAD_REQUEST 
            return resp.write(e)
        
# vim: set ai sts=4 et ts=4 sw=4:
