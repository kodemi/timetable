from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view

from timetable.api.handlers import FlightHandler


flight_handler = Resource(FlightHandler)

urlpatterns = patterns('',
        url(r'^flight/(?P<flight>[^/\.]+)$', flight_handler, {'emitter_format': 'xml'}),
        url(r'^flight/(?P<flight>[^/\.]+).(?P<emitter_format>.+)', flight_handler, name='flight'),
        url(r'^flights$', flight_handler, {'emitter_format': 'xml'}),
        url(r'^flights.(?P<emitter_format>.+)', flight_handler, name='flights'),
        url(r'^$', documentation_view),
)
