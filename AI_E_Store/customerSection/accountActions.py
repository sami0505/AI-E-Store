from .models import Customer, TokenAction, Item, OrderLine, Review
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import date, timedelta
import random

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
        # Check any one of the ordered styles is collected (thus hasOrdered being true)
        for result in results:
            if result.OrderID.IsCollected:
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

# This is the procedure that is used to generate the featured items
def generateFeatured():
    items = Item.objects.all()
    if date.today().weekday() == 5 and len(items) >= 8:
        try:  # It's a monday. Attempt to recalculate QBRs for previously featured items
            featuredDate = timezone.now().date() - timedelta(days=7)
            featuredRecord = FeaturedItems.objects.get(pk=featuredDate)
            preFeatured = featuredRecord.returnItems()

            for item in preFeatured:  # Recalculate QBR for each item featured last week
                orderLines = OrderLine.objects.filter(ItemInstanceID=item, OrderID__DateOfSale__gte=featuredDate, OrderID__DateOfSale__lt=timezone.now().date())
                QBF = len(orderLines)
                allFeatured = FeaturedItems.objects.all()
                dateNotFeatured = None

                for generation in allFeatured:  # Check if the current week contains the item 
                    generationItems = generation.returnItems()
                    if not(item in generationItems):
                        dateNotFeatured = generation.DateUsed
                        break

                if dateNotFeatured == None:
                    # This item has never not been featured. QBR can't be calculated
                    QBR = -1
                else:
                    # The date where the item is not featured was found.
                    orderLines = OrderLine.objects.filter(ItemInstanceID=item, OrderID__DateOfSale__gte=dateNotFeatured, OrderID__DateOfSale__lt=(dateNotFeatured + timedelta(days=7)))
                    QBU = len(orderLines)
                    QBR = QBF / QBU
                    item.QBR = QBR
                    item.save()  # Recalculate and save new QBR

            # Generate the new featured items
            featuredItems = []
            neverFeatured = [itemInstance for itemInstance in itemInstance.objects.filter(QBR__lt=0)]
            itemsDict = {}
            for itemInstance in ItemInstance.objects.all():
                if itemInstance.QBR > 0:
                    itemsDict[itemInstance.ItemInstanceID] = itemInstance.QBR
            itemsDict = sorted(itemsDict.items(), key=itemsDict.get(), reverse=True)

            # Generate 4 Items: Highest QBR
            for i in range(0, 4):
                featuredInstance = ItemInstance.objects.get(pk=list(itemsDict)[i])
                instancesToRemove = ItemInstance.objects.filter(ItemID=featuredInstance.ItemID)
                for instance in instancesToRemove:
                    del itemsDict[instance]
                featuredItems.append(featuredInstance)

            # Generate 2 Items: notFeatured OR 5th / 6th highest QBR
            for i in range(0,2):
                if not neverFeatured:
                    # There are no items are haven't been featured
                    featuredInstance = ItemInstance.objects.get(pk=list(itemsDict)[i])
                else:
                    featuredInstance = neverFeatured.pop()

                instancesToRemove = ItemInstance.objects.filter(ItemID=featuredInstance.ItemID)
                for instance in instancesToRemove:
                    del itemsDict[instance]
                featuredItems.append(featuredInstance)

            # Generate 2 Items: notFeatured OR randomItem
            for i in range(0, 2):
                if not neverFeatured:
                    # There are no items are haven't been featured
                    randomInstanceID = list(itemsDict)[random.randint(0, len(itemsDict))]
                    featuredInstance = ItemInstance.objects.get(pk=randomInstanceID)
                else:
                    featuredInstance = neverFeatured.pop()
                    
                instancesToRemove = ItemInstance.objects.filter(ItemID=featuredInstance.ItemID)
                for instance in instancesToRemove:
                    del itemsDict[instance]
                featuredItems.append(featuredInstance)

            newFeatured = FeaturedItems()
            newFeatured.writeItems(featuredItems)
            newFeatured.save()

        except Exception as error:
            # Something went wrong, likely invalid date for featuredRecord
            if featuredDate.weekday() != 0:
                # Something else went wrong.
                print(f"An Error occurred: {error}")
            else:
                # The "Invalid" featuredDate is a monday, which means that this is likely the first run.
                featuredItems = []
                for i in range(0,8):  # Generate random featured items
                    randomInstanceID = list(itemsDict)[random.randint(0, len(itemsDict))]
                    featuredInstance = ItemInstance.objects.get(pk=randomInstanceID)
                    featuredItems.append(featuredInstance)
                newFeatured = FeaturedItems()
                newFeatured.writeItems(featuredItems)
                newFeatured.save()
        else:
            # Successfully recalculated QBRs and Generated new featured Items.
            print("Successfully Recalibrated QBRs")
            
    else:  # It's either not a monday, or there are not enough items.
        if len(items) < 8:
            # There are not enough items
            print("There are not enough items to make a featured list!")
        else:
            # It's not a monday
            print("It's not a monday yet! Wait for it.")