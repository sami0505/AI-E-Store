from .models import Customer, TokenAction


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
