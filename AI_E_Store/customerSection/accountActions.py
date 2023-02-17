from .models import Customer
import datetime


def registerAccount(form):
    """ This function takes in a form, and registers a user with the info. It also sends an activation email."""
    status = True  # status indicates the status of execution. If an error occurs, the status will be false
    try:
        # Create newAccount and assign attributes from form
        newAccount = Customer.objects.create_user(username=form["Username"], password=form["Password"],
                                                  DateOfBirth=form["DateOfBirth"], DateJoined=datetime.date.today())
        newAccount.Firstname = form["Firstname"]
        newAccount.Surname = form["Surname"]
        newAccount.EmailAddress = form["Email"]
        newAccount.Telephone = form["Telephone"]
        newAccount.Title = form["Title"]
        newAccount.save()

        # TODO Activation
        # TODO Send Email
    except Exception as error:
        status = False
        # TODO Log error
        # TODO Respond
        return error
    else:
        return None
    finally:
        pass
        # TODO Log transaction
