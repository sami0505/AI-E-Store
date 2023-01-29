from django.test import TestCase
from customerSection.models import Customer, Item, Review
import datetime
import unittest
# Create your tests here.

class unit_1_1_Tests(TestCase):
    def test_1_1_1(self):
        """ This is test 1.1.1. """
        try:
            newCustomer = Customer()
            newCustomer.Firstname = "John"
            newCustomer.Surname = "Doe"
            newCustomer.Email = "foo.bar@doemail.org"
            newCustomer.Telephone = "05555555555"
            newCustomer.Username = "johnDoe.01"
            newCustomer.Password = "1@2B3c4."
            newCustomer.Title = "Mr"
            newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
            newCustomer.DateJoined = datetime.date.today()
            newCustomer.save()
        except Exception as error:
            self.fail(f"The test failed because an error occured: {error}")

    def test_1_1_2(self):
        """ This is test 1.1.2 """
        try:
            newCustomer = Customer()
            newCustomer.Firstname = "Vila Bela da Santíssima Trindade"
            newCustomer.Surname = "Fernando del Valle de Catamarcas"
            newCustomer.Email = "ReallyLongEmailThatStretchesForWayTooLong@ButStillValid.mail.org"
            newCustomer.Telephone = "05555555555"
            newCustomer.Username = "vilaCat.01011970"
            newCustomer.Password = "ThisIsARe@llyL0ngPasswordForSome"
            newCustomer.Title = "Lord"
            newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
            newCustomer.DateJoined = datetime.date.today()
            newCustomer.save()
        except Exception as error:
            self.fail(f"The test failed because an error occured: {error}")

    def test_1_1_3(self):
        """ This is test 1.1.3 """
        with self.assertRaises(Exception):
            newCustomer = Customer()
            newCustomer.Firstname = "Vila Bela da Santíssima Trindades"
            newCustomer.Surname = "Fernando del Valles de Catamarcas"
            newCustomer.Email = "ReallyLongEmailThatStretchesForWayTooLong@SeenAsInvalid.email.org"
            newCustomer.Telephone = "055555555555"
            newCustomer.Username = "vilaCats.01011970"
            newCustomer.Password = "ThisWasARe@llyL0ngPasswordForSome"
            newCustomer.Title = "Large"
            newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
            newCustomer.DateJoined = datetime.date.today()
            newCustomer.save()
            self.fail(f"The test failed because an error should have occured!")
    
    def test_1_1_4(self):
        """ This is test 1.1.4 """
        with self.assertRaises(Exception):
            newCustomer = Customer()
            newCustomer.Firstname = "John"
            newCustomer.Surname = "Doe"
            newCustomer.Email = "foo.bar@doemail.org"
            newCustomer.Telephone = "05555555555"
            newCustomer.Username = "johnDoe.01"
            newCustomer.Password = "1@2B3c4."
            newCustomer.Title = "Mr"
            newCustomer.DateOfBirth = datetime.date(0, 1, 1)
            newCustomer.DateJoined = datetime.date(0, 1, 1)
            newCustomer.save()
            self.fail(f"The test failed because an error should have occured!")
    
    def test_1_1_5(self):
        """ This is test 1.1.5 """
        with self.assertRaises(Exception):
            newCustomer = Customer()
            newCustomer.save()
            self.fail(f"The test failed because an error should have occured!")
        
    def test_1_1_6(self):
        """ This is test 1.1.6"""
        with self.assertRaises(Exception):
            newCustomer = Customer()
            newCustomer.Firstname = 1
            newCustomer.Surname = 2
            newCustomer.Email = 3
            newCustomer.Telephone = 4
            newCustomer.Username = 5
            newCustomer.Password = 6
            newCustomer.Title = 7
            newCustomer.DateOfBirth = 8
            newCustomer.DateJoined = 9
            newCustomer.save()
            self.fail(f"The test failed because an error should have occured!")