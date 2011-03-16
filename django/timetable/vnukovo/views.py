from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from timetable.vnukovo.models import Flight

def flights(request):
    flights = Flight.objects.all()
    return render_to_response("vnukovo/flights.html", {
        'flights': flights },
        RequestContext(request))
