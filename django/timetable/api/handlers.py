from django.utils import simplejson
from django import forms
from django.core.exceptions import ValidationError
from piston.handler import BaseHandler
from piston.utils import rc
from django.core import serializers
import json

from vnukovo.models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight

class FlightHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = Flight
    
    @classmethod
    def resource_uri(cls, flight):
        return ('flight', ['json', ])

    def read(self, request, flight=None):
        base = Flight.objects
        if flight:
            return base.get(flight=flight)
        else:
            return base.all()

    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        if 'data' in attrs:
            attrs = json.loads(request.POST.get('data'))
        else:
            return rc.BAD_REQUEST
        try:
            inst = self.model.objects.get(**attrs)
            print 'Duplicate entry: %s' % inst
            return rc.DUPLICATE_ENTRY
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
            inst.save()
            #return serializers.serialize('json', [inst], ensure_ascii=False)
            return inst
        except Exception, e:
            print 'Error: %s' % e
            resp = rc.BAD_REQUEST 
            return resp.write(e)
        
# vim: set ai sts=4 et ts=4 sw=4:
