#-*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

FLIGHT_TYPE_CHOICES = (
    (False, 'Arrival'),
    (True, 'Departure'),
)

AIRPORT_CHOISE = (
    ('VKO', u'Внуково'),
    ('SVO', u'Шереметьево'),
    ('DME', u'Домодедово'),
    ('LED', u'Пулково')
)

class Flight(models.Model):
    airport = models.CharField(max_length=3, choices=AIRPORT_CHOISE)
    flight = models.CharField(max_length=10)
    flight_type = models.BooleanField(choices=FLIGHT_TYPE_CHOICES)
    airline = models.CharField(max_length=70)
    airport_of_departure = models.CharField(max_length=70, default='', blank=True)
    city_of_departure = models.CharField(max_length=70)
    airport_of_arrival = models.CharField(max_length=70, default='', blank=True)
    city_of_arrival = models.CharField(max_length=70)
    flight_status = models.CharField(max_length=20, default='', blank=True)
    datetime_scheduled = models.DateTimeField('Scheduled')
    datetime_estimated = models.DateTimeField('Estimated', null=True, blank=True)
    datetime_actual = models.DateTimeField('Actual', null=True, blank=True)
    terminal = models.CharField(max_length=3, blank=True)
    comment = models.CharField(max_length=250, default='', blank=True)
    checkin_desk = models.CharField('Check-in desk', max_length=10, default='', blank=True)
    
    def __unicode__(self):
        return "%s" % self.flight

    def get_fields(self):
        fields = []
        for field in Flight._meta.fields:
            if field.name == 'flight_type':
                fields.append((field.name, self.get_flight_type_display())) 
            else:
                fields.append((field.name, field.value_to_string(self)))
        return fields

class FlightAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {'fields': ['airport', 'flight', 'flight_type', 'airline', 'flight_status']}),
            ('Airport', {'fields': ['city_of_departure', 'airport_of_departure', 'city_of_arrival', 'airport_of_arrival']}),
            ('Date & Time', {'fields': ['datetime_scheduled', 'datetime_estimated', 'datetime_actual']}),
            (None, {'fields': ['terminal', 'comment', 'checkin_desk']}),
    ]
    list_display = ('flight', 'airline', 'flight_status')

