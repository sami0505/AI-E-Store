from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.template import loader
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import Register, Login, ResetRequest, Reset, ReviewForm
from .accountActions import registerAccount, validateReview, formatRows
from .models import TokenAction, Customer, Review, Item, Style  # Customer is used with TokenAction


# This is the "front page" default view
def index(request):
    itemsShown = []
    query = Item.objects.all().filter()
    rows = formatRows(query)
    context = {"user": request.user, "rows": rows, "mediaURL": settings.MEDIA_ROOT}
    return render(request, "index.html", context)


# This view handles registrations on the webpage.
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


# This view handles review placement.
@login_required(login_url="login")
def review(request):
    if request.method == "POST":
        status = False
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                currentItem = Item.objects.get(pk=form.cleaned_data["ItemID"])
            except Exception as error:  # Something went wrong, most likely an invalid itemID.
                clientError = "Something went wrong with the review.."
                serverError = error
            else:  # Valid Item
                customer = Customer.objects.get(pk=request.user.pk)
                if validateReview(customer, currentItem):
                    # Review is valid, thus is placed.
                    comment = form.cleaned_data["Comment"]
                    stars = form.cleaned_data["StarRating"]
                    currentReview = Review(CustomerID=customer, ItemID=currentItem, StarRating=stars, Comment=comment)
                    status = True
                else:  # Not eligible to review
                    clientError = "You are not eligible to review this item!"
                    serverError = "An ineligible user attempted a review."
        else:  # Form is Invalid
            clientError = "The form submitted was invalid. Try again."
            serverError = "Invalid Form."

        # Status evaluation
        if status:
            currentReview.save()
            messages.success(request, "Review successfully placed!")
            return redirect("/")
        else:
            messages.error(request, clientError)
            print(f"An Error occurred: {serverError}")
            return redirect("/review/")
        # TODO Add logging
    else:  # GET
        form = ReviewForm()
        context = {"form": form}
        return render(request, "review.html", context)


# This view handles requests to reset passwords, not the reset itself
def request_reset(request):
    if request.method == "POST":
        status = True
        form = ResetRequest(request.POST)
        if form.is_valid():
            # Check if account exists
            userEmail = form.cleaned_data["Email"]
            refAccount = Customer.objects.all().filter(email=userEmail)
            if not refAccount:  # Invalid Email
                clientError = "The email given doesn't refer to an existing account."
                serverError = "Invalid Email Reference."
                status = False
        else:  # Invalid form
            clientError = "The form submitted was invalid. Try again."
            serverError = "Invalid Form."
            status = False
        if status:
            newToken = TokenAction.create(1, refAccount[0].pk)
            newToken.save()  # Added password reset token

            subject = "Password Reset Link"
            message = f"Hi, you have requested a password reset. Here is the link: {newToken.getURL()}"
            sender = settings.EMAIL_HOST_USER
            recipient = [userEmail]
            send_mail(subject, message, sender, recipient)
            messages.info(request, "Email sent. Check your emails!")
            return redirect("/")
        else:
            print(f"An Error occurred: {serverError}")
            messages.error(request, clientError)
            return redirect("/resetrequest/")
    else:  # GET
        form = ResetRequest()
        context = {"form": form}
        return render(request, "resetrequest.html", context)


# This view is used to handle log in forms and the following actions to handle success
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


# This view is used to attempt a logout, even if the user isn't logged in
def attempt_logout(request):
    logout(request)
    return redirect("/")


# This view acts as a form of request to delete an account
def deletion(request):
    if request.user.is_authenticated:
        # Go through with token creation
        newToken = TokenAction.create(2, request.user.CustomerID)
        newToken.save()
        messages.info(request, "The link to delete your account should be in your emails.")
        subject = "About your account deletion"
        message = f"Hi, you have requested an account deletion. Here is the link: {newToken.getURL()}"
        sender = settings.EMAIL_HOST_USER
        recipient = [request.user.email]
        send_mail(subject, message, sender, recipient)
        return redirect("/")
    else:
        return HttpResponseNotFound("")  # 404 Error


# This view handles tokens and actions for user verification
def verification(request, token):
    try:
        # Attempt to get the TokenAction of the current token
        currentToken = TokenAction.objects.get(pk=token)
    except Exception as error:
        # Something went wrong (most likely an invalid token)
        print(f"An Error occurred: {error}")
        return redirect("/")

    if request.method == "POST":
        status = True
        form = Reset(request.POST)
        if form.is_valid() and currentToken.Reason == 1:
            # Check if the email matches the userID given
            userEmail = form.cleaned_data["Email"]
            refAccount = Customer.objects.all().filter(email=userEmail)
            expectedID = currentToken.getResetUserID()
            if refAccount and refAccount[0].pk == expectedID:
                # Successful check
                newPassword = form.cleaned_data["NewPassword"]
                action = currentToken.Action + f"('{newPassword}');c.save()"  # Adding the newPassword to the action str
                exec(action)
                currentToken.delete()
                messages.success(request, "Your password has been successfully reset!")
                # TODO Use Logging
            else:  # Invalid Email
                status = False
                serverError = "The referenced account doesn't exist or isn't the correct user."
        else:  # Invalid Form
            status = False
            serverError = "Invalid Form."
        if not status:  # Error occurred
            messages.error(request, "Something went wrong. Make sure the inputted email address is correct!")
            print(serverError)
        return redirect("/")
    else:  # GET
        context = {}
        if currentToken.Reason == 1:
            # Reset Password
            form = Reset()
            context = {"form": form}
            return render(request, "reset.html", context)
        else:
            # The action will now be executed. Afterwards, redirect to index
            exec(currentToken.Action)
            currentToken.delete()
            return redirect("/")

# Turns a query parameter from a string that could be invalid to an integer
def sanitizeParam(param):
    if param != None:
        try:
            param = int(param)
        except:  # The parameter is not an integer
            param = 0
    else:  # The parameter hasn't been provided
        param = 0

    return param
    

# The category view is a type of discrete result browsing. The only outcomes from category are in the below set
categorySet = {"coats", "jackets", "shirts", "t-shirts", "shorts", "trousers", "hoodies", "sweaters", "hats", "socks"}
def category(request, currentCategory):
    if currentCategory in categorySet:
        sortType = request.GET.get("sort")  # Get the user's sorting preference
        sortType = sanitizeParam(sortType) # Ensure valid sortType

        itemsShown = []  # Valid category
        query = Item.objects.filter(Category=currentCategory.title())
        rows = formatRows(query)
        context = {"user": request.user, "category": currentCategory.title() ,"rows": rows,"mediaURL": settings.MEDIA_ROOT}
        return render(request, "category.html", context)
    else:  # Invalid category
        return redirect("/")
    

# This function returns the search results of the query of the search bar
def search(request):
    if request.method == "GET":
        searchString = request.GET.get("search")  # Get user's search text
        sortType = request.GET.get("sort")  # Get the user's sorting preference
        sortType = sanitizeParam(sortType)  # Ensure valid sortType

        query = Item.objects.filter(Title__icontains=searchString)
        rows = formatRows(query, sortType)
        context = {"user": request.user,"rows": rows,"mediaURL": settings.MEDIA_ROOT}
        return render(request, "search.html", context)
    else:  # POST request
        return redirect("/")

# This view returns a detailed look at a certain item
def detailed(request, itemID):
    if request.method == "GET":
        # Get item, styles and reviews for context
        item = Item.objects.get(pk=itemID)
        styles = list(item.getStyles())
        reviews = list(Review.objects.filter(ItemID=itemID))
        meanRating = item.getMeanRating()

        # Get style index to acquire image to show, sanitize it, use it
        styleIndex = request.GET.get("style")
        styleIndex = sanitizeParam(styleIndex)            
        currentStyle = styles[styleIndex]

        # Check if the user is eligible to review this item
        if request.user.is_authenticated:
            customer = Customer.objects.get(pk=request.user.pk)
            validity = validateReview(customer, item)
            validity = True
        else:
            validity = False

        context = {"user": request.user, "mediaURL": settings.MEDIA_URL, "item": item, "styles": styles, "reviewCount": len(reviews), 
                "reviews": reviews, "currentStyle": currentStyle, "isEligible": validity, "stars": meanRating}
        return render(request, "detailed.html", context)
    else:  # POST
        # TODO handle this
        pass


# This view shows the user's profile data, also giving the option to delete the account
@login_required(login_url="/login/")
def profile(request):
    context = {"user": request.user, "mediaURL": settings.MEDIA_ROOT}
    return render(request, "profile.html", context)

# This view adds the given item from the url to the logged in user's basket
@login_required(login_url="login")
def addToBasket(request, styleID):
    try:
        styleAdded = Style.objects.get(pk=styleID)
    except:  # An error occured. Most likely an incorrent styleID
        pass
    else:
        customer = Customer.objects.get(pk=request.user.pk)
        customer.basket += f"{styleID},"
        customer.save()
        messages.success(request, "Item successfully added to basket!")
    return redirect(request.META.get('HTTP_REFERER'))

# This view displays the user's basket.
@login_required(login_url="login")
def basket(request):
    customer = Customer.objects.get(pk=request.user.pk)
    basket = customer.basket.split(",")
    basket.remove("")
    styles = [Style.objects.get(pk=styleID) for styleID in basket]
    context = {"user": request.user, "styles": styles, "mediaURL": settings.MEDIA_ROOT}
    return render(request, "basket.html", context)

# This view results in the removal of the style whose ID is in the URL 
@login_required(login_url="login")
def removeFromBasket(request, styleID):
    customer = Customer.objects.get(pk=request.user.pk)
    basket = customer.basket.split(",")
    if str(styleID) in basket:
        basket.remove(str(styleID))
        newBasket = ",".join(basket)
        customer.basket = newBasket
        customer.save()
    return redirect("/basket/")

# This view adds the given item from the url to the logged in user's wishlist
@login_required(login_url="login")
def addToWishlist(request, styleID):
    try:
        styleAdded = Style.objects.get(pk=styleID)
    except:  # An error occured. Most likely an incorrent styleID
        pass
    else:
        customer = Customer.objects.get(pk=request.user.pk)
        customer.wishlist += f"{styleID},"
        customer.save()
        messages.success(request, "Item successfully added to wishlist!")
    return redirect("/")

# This view displays the user's wishlist.
@login_required(login_url="login")
def wishlist(request):
    customer = Customer.objects.get(pk=request.user.pk)
    wishlist = customer.wishlist.split(",")
    wishlist.remove("")
    styles = [Style.objects.get(pk=styleID) for styleID in wishlist]
    context = {"user": request.user, "styles": styles, "mediaURL": settings.MEDIA_ROOT}
    return render(request, "wishlist.html", context)

# This view results in the removal of the style whose ID is in the URL
@login_required(login_url="login")
def removeFromWishlist(request, styleID):
    customer = Customer.objects.get(pk=request.user.pk)
    wishlist = customer.wishlist.split(",")
    if str(styleID) in wishlist:
        wishlist.remove(str(styleID))
        newWishlist = ",".join(wishlist)
        customer.wishlist = newWishlist
        customer.save()
    return redirect("/wishlist/")
