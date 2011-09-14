from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view

from api.handlers import FlightHandler #, RecentFlightHandler


flight_handler = Resource(FlightHandler)
#recent_flight_handler = Resource(RecentFlightHandler)

urlpatterns = patterns('',
        url(r'^flight/(?P<flight>[^/\.]+)$', flight_handler, {'emitter_format': 'json'}),
        url(r'^flight/(?P<flight>[^/\.]+).(?P<emitter_format>.+)', flight_handler, name='flight'),
        url(r'^flights$', flight_handler, {'emitter_format': 'xml'}),
        url(r'^flights/recent$', flight_handler, {'emitter_format': 'xml'}),
        url(r'^flights/recent.(?P<emitter_format>.+)$', flight_handler, {'emitter_format': 'json'}),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/$', flight_handler, {'emitter_format': 'json'}),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/flights', flight_handler, {'emitter_format': 'json'}),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/flights.(?P<emitter_format>.+)', flight_handler, name='date_flights'),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/(?P<ffrom>[^/\.]+)_(?P<fto>[^/\.]+)/flights', flight_handler, {'emitter_format': 'json'}),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/(?P<ffrom>[^/\.]+)_(?P<fto>[^/\.]+)/(?P<flight>[^/\.]+)', flight_handler, {'emitter_format': 'json'}),
        url(r'^(?P<month>\d{2})/(?P<day>\d{2})/(?P<flight>[^/\.]+).(?P<emitter_format>.+)', flight_handler, name='date_flight'),
        url(r'^$', documentation_view),
)
