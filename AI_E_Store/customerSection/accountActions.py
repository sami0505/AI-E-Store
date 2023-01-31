from .models import Customer
import datetime
import bcrypt

salt = b"$2b$12$Mr8cYTjur7w4gUtGG.P7Mu"

def registerAccount(form):
    status = True
    try:
        newAccount = Customer()
        newAccount.Firstname = form["Firstname"]
        newAccount.Surname = form["Surname"]
        newAccount.Email = form["Email"]
        newAccount.Telephone = form["Telephone"]
        newAccount.Username = form["Username"]
        unhashedPass = str.encode(form["Password"]) # Turns password into array of bytes
        hashedPass = bcrypt.hashpw(unhashedPass, salt) # Stores hashed password
        newAccount.Password = hashedPass.decode() # Decodes back to string
        newAccount.Title = form["Title"]
        newAccount.DateOfBirth = form["DateOfBirth"]
        newAccount.DateJoined = datetime.date.today()
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