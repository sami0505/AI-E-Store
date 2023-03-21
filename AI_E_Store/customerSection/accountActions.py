from .models import Customer, TokenAction, FeaturedItems, OrderLine, Item, ItemInstance
from datetime import date, timedelta
from django.utils import timezone
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
        # TODO Send Email
    except Exception as error:
        status = False
        # TODO Log error
        return error
    else:
        return None
    finally:
        pass
        # TODO Log transaction

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
            # Successfully recalculated QBRs without any errors
            print("Successfully Recalibrated QBRs")
            newFeatured.save()
    else:
        if len(items) < 8:
            # There are not enough items
            print("There are not enough items to make a featured list!")
        else:
            # It's not a monday
            print("It's not a monday yet! Wait for it.")