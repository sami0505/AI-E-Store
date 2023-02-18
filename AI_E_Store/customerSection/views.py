from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, logout
from .forms import Register, Login
from .accountActions import registerAccount
from .models import TokenAction, Customer


def index(request):
    context = {"user": request.user}  # FIXME the logged in doesn't show
    return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        # The form is contained in the POST
        form = Register(request.POST)
        if form.is_valid():
            # The form is valid
            error = registerAccount(form.cleaned_data)  # TODO add proper responses to errors
            if error is not None:
                print(f"An Error occurred: {error}")
        else:
            # The form is invalid
            print("An Error occurred: Invalid Form")
        return redirect("/")  # Redirects back to index
    else:
        # Create a form and add it to the context Dict
        form = Register()
        context = {"form": form}
        return render(request, "registration.html", context)


def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            try:
                authenticate(username=form.cleaned_data["Username"], password=form.cleaned_data["Password"])
            except Exception as error:
                print(f"An Error occurred: {error}")
                return redirect("/login/")
            else:
                return redirect("/")
        else:
            print("An Error occurred: Invalid Form")
            return redirect("/login/")
    else:
        form = Login()
        context = {"form": form}
        return render(request, "login.html", context)


def attempt_logout(request):
    logout(request)
    return redirect("/")


def verification(request, token):
    try:
        # Attempt to get the TokenAction of the current token
        currentToken = TokenAction.objects.get(pk=token)
    except Exception as error:
        # Something went wrong (most likely an invalid token)
        print(f"An Error occurred: {error}")
        return redirect("/")

    if request.method == "POST":
        pass        # TODO add password reset handling
    else:
        context = {}
        if currentToken.Reason == 1:
            pass    # TODO add password reset handling
        else:
            # The action will now be executed. After, redirect to index
            exec(currentToken.Action)
            currentToken.delete()
            return redirect("/")
