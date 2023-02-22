from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.template import loader
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .forms import Register, Login, ResetRequest, Reset
from .accountActions import registerAccount
from .models import TokenAction, Customer  # Customer is used with TokenAction


def index(request):
    context = {"user": request.user}
    return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        # The submission is contained in the POST
        form = Register(request.POST)
        if form.is_valid():
            # The form is valid
            error = registerAccount(form.cleaned_data)
            if error is None:
                messages.success(request, "Registration successful. Check your email.")
            else:
                messages.error(request, "There was a problem with your registration. Try again.")
                print(f"An Error occurred: {error}")
        else:
            # The form is invalid
            messages.error(request, "There was a problem with your registration. Try again.")
            print("An Error occurred: Invalid Form")
        return redirect("/")  # Redirects back to index
    else:
        # Create a form and add it to the context Dict
        form = Register()
        context = {"form": form}
        return render(request, "registration.html", context)


# This view handles requests to reset passwords, not the reset itself
def request_reset(request):  # TODO Refactor pass reset with status
    if request.method == "POST":
        form = ResetRequest(request.POST)
        if form.is_valid():
            userEmail = form.cleaned_data["Email"]
            refAccount = Customer.objects.all().filter(email=userEmail)
            if refAccount:
                newToken = TokenAction.create(1, refAccount[0].pk)
                newToken.save()
                # TODO SEND EMAIL
                messages.info(request, "Email sent. Check your emails!")
                return redirect("/")
            else:  # Invalid Email
                messages.error(request, "THATS NOT EXIST")
                print("Error dont exist")  # TODO proper errors pls
                return redirect("/resetrequest/")
        else:  # Invalid form
            messages.error(request, "BAD FORM")
            print("Goofy Form error")
            return redirect("/resetrequest/")
    else:  # GET
        form = ResetRequest()
        context = {"form": form}
        return render(request, "resetrequest.html", context)


def attempt_login(request):
    if request.method == "POST":  # POST Request
        status = True
        userID = None  # Used for logs
        form = Login(request.POST)

        # Form processing
        if form.is_valid():  # Form is valid
            try:
                user = authenticate(username=form.cleaned_data["Username"], password=form.cleaned_data["Password"])
                if user is not None:  # Correct Credentials
                    login(request, user)
                    userID = user.CustomerID
                else:  # Authentication Error
                    raise Exception("Authentication Failed!")
            except Exception as error:  # Something went wrong during login
                status = False
                print(f"An Error occurred: {error}")
        else:  # Form is invalid
            status = False
            print("An Error occurred: Invalid Form")

        # Status handling
        if status:
            return redirect("/")
        else:
            messages.error(request, "An error occurred with the login. Make sure your credentials are " +
                           "correct and that your account is activated. Otherwise, try later.")
            return redirect("/login/")
        # TODO Logging
    else:  # GET Request
        form = Login()
        context = {"form": form}
        return render(request, "login.html", context)


def attempt_logout(request):
    logout(request)
    return redirect("/")


def deletion(request):
    if request.user.is_authenticated:
        # Go through with token creation
        newToken = TokenAction.create(2, request.user.CustomerID)
        newToken.save()
        messages.info(request, "The link to delete your account should be in your emails.")
        # TODO email functionality
        return redirect("/")
    else:
        return HttpResponseNotFound("")  # 404 Error


def verification(request, token):  # TODO Refactor pass reset with status
    try:
        # Attempt to get the TokenAction of the current token
        currentToken = TokenAction.objects.get(pk=token)
    except Exception as error:
        # Something went wrong (most likely an invalid token)
        print(f"An Error occurred: {error}")
        return redirect("/")

    if request.method == "POST":
        form = Reset(request.POST)        # TODO add password reset handling
        if form.is_valid():
            # Check if the email matches the userID given
            userEmail = form.cleaned_data["Email"]
            refAccount = Customer.objects.all().filter(email=userEmail)
            expectedID = currentToken.getResetUserID()
            if refAccount and refAccount[0].pk is expectedID:  # FIXME Error I dont exist keeps outputting 
                newPassword = form.cleaned_data["NewPassword"]
                action = action + f"({newPassword})"  # TODO Explain this pls
                exec(action)
                currentToken.delete()
                messages.success(request, "PASSWORD RESET!")
            else:  # Invalid Email
                messages.error(request, "Something went wrong. Make sure the inputted email address is correct!")
                print("Error I dont exist")  # TODO proper errors pls
        else:   # TODO fix error messages
            messages.error(request, "Something went wrong. Make sure the inputted email address is correct!")
            print("INVALID FORM")
        return redirect("/")
    else:
        context = {}
        if currentToken.Reason == 1:
            form = Reset()    # TODO add password reset handling
            context = {"form": form}
            return render(request, "reset.html", context)
        else:
            # The action will now be executed. After, redirect to index
            exec(currentToken.Action)
            currentToken.delete()
            return redirect("/")
