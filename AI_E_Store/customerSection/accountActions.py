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

def formatRows(query, sortingMethod=0):
    """ Given a search query result, it returns its formatted version in rows. Sorting Method Codes are as follows:
        0: Alphabetical A-Z
        1: Alphabetical Z-A
        2: Price Low-High
        3: Price High-Low
        default: 0
    """
    if len(query) > 0:
        itemsShown = []
        # Each itemEntry is a list of a displayed item. All items from query are put in itemsShown
        # itemEntry format: 0: ItemID, 1: Price, 2: Title, 3: HighResImg
        for item in query:
            if len(item.getStyles()) > 0:
                style = item.getStyles()[0]
                itemEntry = [item.ItemID, item.Price, item.Title, style.HighResImg.url]
                itemsShown.append(itemEntry)

        # Sorting the itemsShown based on the Sort Method. The result is the items being sorted correctly.
        if sortingMethod < 4 and sortingMethod >= 0:
            if sortingMethod < 2:  # Alphabetical Sort
                itemsShown.sort(key=lambda x: x[2], reverse=sortingMethod)
            else:  # Price Sort
                reversed = sortingMethod - 2
                itemsShown.sort(key=lambda x: x[1], reverse=reversed)
        else:  # Invalid sorting method value
            print("Invalid value, using default...")
            itemsShown.sort(key=lambda x: x[2])

        # itemsShown is formatted to a row format suitable for
        rows = []
        currentRow = []
        # Each item is added to current
        for item in itemsShown:
            if len(currentRow) == 4:
                rows.append(currentRow)
                currentRow = []
            currentRow.append(item)
        # Adding the last row
        if currentRow:
            rows.append(currentRow)
        # Rows is a list of lists (rows) that each contain 4 or less itemEntries
        return rows
    else:
        return 0
