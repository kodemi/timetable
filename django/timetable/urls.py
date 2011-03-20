from django.conf.urls.defaults import * 
from django.contrib import admin
from timetable.vnukovo.models import Flight, FlightAdmin

admin.autodiscover()
admin.site.register(Flight, FlightAdmin)

urlpatterns = patterns('',
    # Examples:
    # url(r'^', 'timetable.views.home', name='home'),
    # url(r'^timetable/', include('timetable.foo.urls')),
    (r'^', include('timetable.vnukovo.urls')),
    (r'^api/', include('timetable.api.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
