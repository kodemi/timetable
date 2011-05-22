from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from timetable.vnukovo.models import Flight

def flights(request, mobile=False):
    flights = Flight.objects.all()
    if mobile:
        return render_to_response("vnukovo/mobile.html", {
            'flights': flights },
            RequestContext(request))
    else:
        return render_to_response("vnukovo/flights.html", {
            'flights': flights },
            RequestContext(request))

def flights_new(request, mobile=False):
    return render_to_response("vnukovo/flights1.html", {},
            RequestContext(request))