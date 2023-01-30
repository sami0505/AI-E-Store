from django import forms

class Register(forms.Form):
    Firstname = forms.CharField(max_length=100)