from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Passenger
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated:
        return render(request, "flights/login.html", {"message":None})
    context = {
        "flights": Flight.objects.all(),
        "user": request.user
        }
    return render(request, "flights/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/login.html", {"message":"Invalid credentials"})

def logout_view(request):
    logout(request)
    return render(request, "flights/login.html", {"message":"Logged out"})

def flight(request, flight_id):
    if not request.user.is_authenticated:
        return render(request, "flights/login.html", {"message":None})    
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist!")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all().order_by('first')
        }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    if not request.user.is_authenticated:
        return render(request, "flights/login.html", {"message":None})       
    try:
        passenger_id  = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message":"No selection."})        
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message":"No passenger."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message":"No flight."})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
