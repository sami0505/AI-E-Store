from django import forms

# This defines the dropdown
# first value is actual value
# second value is the one shown to the user
titleChoices = [
        ("mr" , "Mr"),
        ("mrs" , "Mrs"),
        ("ms" , "Ms"),
        ("lord" , "Lord"),
        ("large" , "Large") # Large is INVALID input
        ] 

class Register(forms.Form):
    # This results in a dropdown instead of an input box
    Title = forms.CharField(label="Title:", widget = forms.Select(choices=titleChoices) )
    
    Firstname = forms.CharField(max_length=32)
    Surname = forms.CharField(max_length=32)
    Email = forms.CharField(max_length=64)
    Telephone = forms.CharField(max_length=11)
    Username = forms.CharField(max_length=16)
    Password = forms.CharField(max_length=60)
    DateOfBirth = forms.DateField()