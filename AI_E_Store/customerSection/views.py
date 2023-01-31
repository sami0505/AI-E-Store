from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import Register
from .accountActions import registerAccount
# Create your views here.

def index(request):
    context = {}
    return render(request, "index.html", context)
    
def register(request):
    if request.method == "POST":
        form = request.POST
        registerAccount(form)
        return redirect("/") # Redirects back to index
    else:
        form = Register()
        context = {"form": form}
        return render(request, "registration.html", context)