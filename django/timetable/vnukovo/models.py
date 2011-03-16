from django.db import models
from django.contrib import admin

class Flight(models.Model):
    flight = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    airport_of_departure = models.CharField(max_length=50)
    airport_of_arrival = models.CharField(max_length=50)
    flight_status = models.CharField(max_length=20, default='', blank=True)
    datetime_scheduled = models.DateTimeField('Scheduled')
    datetime_estimated = models.DateTimeField('Estimated', null=True, blank=True)
    datetime_actual = models.DateTimeField('Actual', null=True, blank=True)
    terminal = models.CharField(max_length=3)
    comment = models.CharField(max_length=250, default='', blank=True)
    
    def __unicode__(self):
        return "%s" % self.flight

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Flight._meta.fields]

class FlightAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields': ['flight', 'airline', 'flight_status']}),
            ('Airport', {'fields': ['airport_of_departure', 'airport_of_arrival']}),
            ('Date & Time', {'fields': ['datetime_scheduled', 'datetime_estimated', 'datetime_actual']}),
            (None, {'fields': ['terminal', 'comment']}),
    ]
    list_display = ('flight', 'airline', 'flight_status')


# vim: set ai sts=4 et ts=4 sw=4:
