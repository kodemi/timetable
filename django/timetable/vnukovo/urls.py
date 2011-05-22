from django.conf.urls.defaults import *

urlpatterns = patterns('timetable.vnukovo.views',
        url(r'^$', 'flights', name='vnukovo-flights'),
        url(r'^new$', 'flights_new'),
        url(r'^mobile$', 'flights', {'mobile': True}),
)
