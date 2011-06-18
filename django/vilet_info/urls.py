from django.conf.urls.defaults import * 
from django.contrib import admin
from vnukovo.models import Flight, FlightAdmin

admin.autodiscover()
admin.site.register(Flight, FlightAdmin)

urlpatterns = patterns('',
    # Examples:
    # url(r'^', 'timetable.views.home', name='home'),
    # url(r'^timetable/', include('timetable.foo.urls')),
    (r'^', include('vnukovo.urls')),
    (r'^api/', include('api.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
