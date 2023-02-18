from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import Register
from .accountActions import registerAccount
from .models import TokenAction, Customer


def index(request):
    context = {}
    return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        # The form is contained in the POST
        form = request.POST
        error = registerAccount(form)  # TODO add proper responses to errors
        if error is not None:
            print(f"An Error occurred: {error}")
        return redirect("/")  # Redirects back to index
    else:
        # Create a form and add it to the context Dict
        form = Register()
        context = {"form": form}
        return render(request, "registration.html", context)


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
