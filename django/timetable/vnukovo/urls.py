from django.conf.urls.defaults import *

urlpatterns = patterns('timetable.vnukovo.views',
        url(r'^$', 'flights', name='vnukovo-flights'),
)
