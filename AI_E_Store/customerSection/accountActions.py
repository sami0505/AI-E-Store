from .models import Customer, TokenAction, Item, OrderLine, Order, Review
from django.conf import settings
from django.core.mail import send_mail


def registerAccount(form):
    """ This function takes in a form, and registers a user with the info. It also sends an activation email."""
    status = True  # status indicates the status of execution. If an error occurs, the status will be false
    try:
        # Create newAccount and assign attributes from form
        newAccount = Customer.objects.create_user(username=form["Username"], email=form["Email"],
                                                  password=form["Password"], DateOfBirth=form["DateOfBirth"],
                                                  Firstname=form["Firstname"], Surname=form["Surname"],
                                                  Telephone=form["Telephone"], Title=form["Title"])
        newToken = TokenAction.create(0, newAccount.pk)
        newToken.save()
        subject = "Verify Account Registration"
        message = f"Hi, you have requested an account registration. Here is the link: {newToken.getURL()}"
        sender = settings.EMAIL_HOST_USER
        recipient = [newAccount.email]
        send_mail(subject, message, sender, recipient)
    except Exception as error:
        status = False
        # TODO Log error
        return error
    else:
        return None
    finally:
        pass
        # TODO Log transaction


def validateReview(user, item):
    """ Given an item and a user, this function will check if the customer is eligible to review the item,
    and return a boolean result of eligibility."""
    hasOrdered = False
    # Check if any style of item has been ordered by the given user.
    for style in item.getStyles():
        results = OrderLine.objects.all().filter(OrderID__CustomerID=user, StyleID=style)
        if results.exists():
            hasOrdered = True
            break

    # Every style has been queried. Check if item has already been reviewed by user
    if hasOrdered:
        hasReviewed = Review.objects.filter(CustomerID=user, ItemID=item).exists()
        return not hasReviewed
    else:
        return False
