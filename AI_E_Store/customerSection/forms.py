from django import forms

# This defines the dropdown
# first value is actual value
# second value is the one shown to the user
titleChoices = [
    ("mr", "Mr"),
    ("mrs", "Mrs"),
    ("ms", "Ms"),
    ("lord", "Lord"),
    ("large", "Large")  # Large is INVALID input
]


class Register(forms.Form):
    # This results in a dropdown instead of an input box
    Title = forms.CharField(label="Title:", widget=forms.Select(choices=titleChoices))
    Firstname = forms.CharField(max_length=32)
    Surname = forms.CharField(max_length=32)
    Email = forms.EmailField(max_length=64)
    Telephone = forms.CharField(max_length=11)
    Username = forms.CharField(max_length=16)
    Password = forms.CharField(max_length=60)
    DateOfBirth = forms.DateField(label="Date Of Birth:")


class Login(forms.Form):
    Username = forms.CharField(max_length=16)
    Password = forms.CharField(max_length=60)


class ResetRequest(forms.Form):
    Email = forms.EmailField(max_length=64)


class Reset(forms.Form):
    Email = forms.EmailField(max_length=64)
    NewPassword = forms.CharField(max_length=60, label="New Password")


class ReviewForm(forms.Form):
    ItemID = forms.IntegerField(min_value=0, max_value=999999999)
    StarRating = forms.IntegerField(min_value=0, max_value=5, label="Star Rating")
    Comment = forms.CharField(max_length=256, widget=forms.Textarea())
