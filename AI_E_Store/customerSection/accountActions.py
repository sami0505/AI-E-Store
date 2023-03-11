from .models import Customer, TokenAction, FeaturedItems, OrderLine
from datetime import date, timedelta
from django.utils import timezone

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

# Foo Bar
def generateFeatured():
    if date.today().weekday() == 5:
        try:  # It's a monday
            featuredDate = timezone.now().date() - timedelta(days=7)
            featuredRecord = FeaturedItems.objects.get(pk=featuredDate)
            preFeatured = featuredRecord.returnItems()
            for item in preFeatured:  # Recalculate QBR
                orderLines = OrderLine.objects.filter(ItemInstanceID=item, OrderID__DateOfSale__gte=featuredDate, OrderID__DateOfSale__lt=timezone.now().date())
                QBF = len(orderLines)
                allFeatured = FeaturedItems.objects.all()
                dateNotFeatured = None
                for generation in allFeatured:
                    generationItems = generation.returnItems()
                    if not(item in generationItems):
                        dateNotFeatured = generation.DateUsed
                        break
                if dateNotFeatured == None:
                    # It has never not been featured. QBR can't be calculated
                    # To solve that, making its QBR -1 removes the need for a QBR
                    QBR = -1
                else:
                    orderLines = OrderLine.objects.filter(ItemInstanceID=item, OrderID__DateOfSale__gte=dateNotFeatured, OrderID__DateOfSale__lt=(dateNotFeatured + timedelta(days=7)))
                    QBU = len(orderLines)
                    QBR = QBF / QBU
                    item.QBR = QBR

        except Exception as error:
            # Something went wrong, likely invalid date for featuredRecord
            if featuredDate.weekday() == 0:
                # The "Invalid" featuredDate is a monday, which means that this is likely the first run.
                pass
            else:
                # Something else went wrong.
                print(f"An Error occurred: {error}")
        else:
            # Successfully recalculated QBRs without any errors
            print("Successfully Recalibrated QBRs")
    else:
        print("It's not a monday yet! Wait for it.")