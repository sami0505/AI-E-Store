from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import Register
# Create your views here.

def index(request):
    form = Register()
    context = {}
    return render(request, "index.html", context)
    
def register(request):
    if request.method == "POST":
        form = request.POST
        return HttpResponse(form["Firstname"])
    else:
        form = Register()
        context = {"form": form}
        return render(request, "registration.html", context)