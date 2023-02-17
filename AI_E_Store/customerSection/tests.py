from django.test import TestCase
from customerSection.models import Customer, Item, Review, Order
import datetime
import bcrypt
import unittest
# Create your tests here.

# class unit_1_1_Tests(TestCase):
#     def test_1_1_1(self):
#         """ This is test 1.1.1. """
#         try:
#             newCustomer = Customer()
#             newCustomer.Firstname = "John"
#             newCustomer.Surname = "Doe"
#             newCustomer.Email = "foo.bar@doemail.org"
#             newCustomer.Telephone = "05555555555"
#             newCustomer.Username = "johnDoe.01"
#             newCustomer.Password = "1@2B3c4."
#             newCustomer.Title = "Mr"
#             newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
#             newCustomer.DateJoined = datetime.date.today()
#             newCustomer.save()
#         except Exception as error:
#             self.fail(f"The test failed because an error occured: {error}")

#     def test_1_1_2(self):
#         """ This is test 1.1.2 """
#         try:
#             newCustomer = Customer()
#             newCustomer.Firstname = "Vila Bela da Santíssima Trindade"
#             newCustomer.Surname = "Fernando del Valle de Catamarcas"
#             newCustomer.Email = "ReallyLongEmailThatStretchesForWayTooLong@ButStillValid.mail.org"
#             newCustomer.Telephone = "05555555555"
#             newCustomer.Username = "vilaCat.01011970"
#             newCustomer.Password = "ThisIsARe@llyL0ngPasswordForSome"
#             newCustomer.Title = "Lord"
#             newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
#             newCustomer.DateJoined = datetime.date.today()
#             newCustomer.save()
#         except Exception as error:
#             self.fail(f"The test failed because an error occured: {error}")

#     def test_1_1_3(self):
#         """ This is test 1.1.3 """
#         with self.assertRaises(Exception):
#             newCustomer = Customer()
#             newCustomer.Firstname = "Vila Bela da Santíssima Trindades"
#             newCustomer.Surname = "Fernando del Valles de Catamarcas"
#             newCustomer.Email = "ReallyLongEmailThatStretchesForWayTooLong@SeenAsInvalid.email.org"
#             newCustomer.Telephone = "055555555555"
#             newCustomer.Username = "vilaCats.01011970"
#             newCustomer.Password = "ThisWasARe@llyL0ngPasswordForSome"
#             newCustomer.Title = "Large"
#             newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
#             newCustomer.DateJoined = datetime.date.today()
#             newCustomer.save()
#             self.fail(f"The test failed because an error should have occured!")
    
#     def test_1_1_4(self):
#         """ This is test 1.1.4 """
#         with self.assertRaises(Exception):
#             newCustomer = Customer()
#             newCustomer.Firstname = "John"
#             newCustomer.Surname = "Doe"
#             newCustomer.Email = "foo.bar@doemail.org"
#             newCustomer.Telephone = "05555555555"
#             newCustomer.Username = "johnDoe.01"
#             newCustomer.Password = "1@2B3c4."
#             newCustomer.Title = "Mr"
#             newCustomer.DateOfBirth = datetime.date(999, 1, 1)
#             newCustomer.DateJoined = datetime.date(999, 1, 1)
#             newCustomer.save()
#             self.fail(f"The test failed because an error should have occured!")
    
#     def test_1_1_5(self):
#         """ This is test 1.1.5 """
#         with self.assertRaises(Exception):
#             newCustomer = Customer()
#             newCustomer.save()
#             self.fail(f"The test failed because an error should have occured!")
        
#     def test_1_1_6(self):
#         """ This is test 1.1.6"""
#         with self.assertRaises(Exception):
#             newCustomer = Customer()
#             newCustomer.Firstname = 1
#             newCustomer.Surname = 2
#             newCustomer.Email = 3
#             newCustomer.Telephone = 4
#             newCustomer.Username = 5
#             newCustomer.Password = 6
#             newCustomer.Title = 7
#             newCustomer.DateOfBirth = 8
#             newCustomer.DateJoined = 9
#             newCustomer.save()
#             self.fail(f"The test failed because an error should have occured!")

# class unit_1_5_Tests(TestCase):
#     def test_1_5_1(self):
#         """ This is test 1.5.1 """
#         try:
#             newCustomer = Customer()
#             newCustomer.Firstname = "John"
#             newCustomer.Surname = "Doe"
#             newCustomer.Email = "foo.bar@doemail.org"
#             newCustomer.Telephone = "05555555555"
#             newCustomer.Username = "johnDoe.01"
#             newCustomer.Password = "1@2B3c4."
#             newCustomer.Title = "Mr"
#             newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
#             newCustomer.DateJoined = datetime.date.today()
#             newCustomer.save()

#             newOrder = Order()
#             newOrder.CustomerID = newCustomer
#             newOrder.DateOfSale = datetime.date.today()
#             newOrder.PaymentMethod = "Debit Card"
#             newOrder.Postcode = "SW1A2AA"
#             newOrder.AddressLine1 = "10 Downing St"
#             newOrder.City = "London"
#             newOrder.save()
#         except Exception as error:
#             self.fail(f"The test failed because an error occured: {error}")

# class unit_1_6_Tests(TestCase):
#     def setUp(self):
#         """ This defines a consistent record! """
#         self.newCustomer = Customer()
#         self.newCustomer.Firstname = "John"
#         self.newCustomer.Surname = "Doe"
#         self.newCustomer.Email = "foo.bar@doemail.org"
#         self.newCustomer.Telephone = "05555555555"
#         self.newCustomer.Username = "johnDoe.01"
#         self.newCustomer.Password = "1@2B3c4."
#         self.newCustomer.Title = "Mr"
#         self.newCustomer.DateOfBirth = datetime.date(1970, 1, 1)
#         self.newCustomer.DateJoined = datetime.date.today()
        
#         self.newCustomer1 = Customer()
#         self.newCustomer1.Firstname = "Jane"
#         self.newCustomer1.Surname = "Doe"
#         self.newCustomer1.Email = "bar.foo@doemail.org"
#         self.newCustomer1.Telephone = "06666666666"
#         self.newCustomer1.Username = "janeDoe.01"
#         self.newCustomer1.Password = "1234"
#         self.newCustomer1.Title = "Mrs"
#         self.newCustomer1.DateOfBirth = datetime.date(1970, 1, 1)
#         self.newCustomer1.DateJoined = datetime.date.today()
        
#         self.newCustomer.save()
#         self.newCustomer1.save()
#         return super().setUp()

#     def test_1_6_1(self):
#         """ This is test 1.6.1 """
#         readCustomer = (Customer.objects.filter(Username = "johnDoe.01"))[0]
#         errorMessage = "The value retrieved and the value in the database are not the same!"
#         self.assertEqual(self.newCustomer, readCustomer, errorMessage)
    
#     def test_1_6_2(self):
#         """ This is test 1.6.2 """
#         readCustomers = Customer.objects.filter(DateOfBirth = datetime.date(1970, 1, 1))
#         errorMessage = "The number of objects that fit query are inaccurate!"
#         self.assertEqual(len(readCustomers), 2, errorMessage)
    
#     def test_1_6_3(self):
#         """ This is test 1.6.3 """
#         readCustomer = Customer.objects.filter(DateOfBirth = datetime.date(1970, 2, 2))
#         errorMessage = "A non existent user was found! That's wrong!"
#         self.assertEqual(len(readCustomer), 0, errorMessage)

#     def test_1_6_4(self):
#         """ This is test 1.6.4 """
#         readCustomers = Customer.objects.filter()
#         self.assertEqual(len(readCustomers), 2, "Not all records were found!")

#     def test_1_6_5(self):
#         """ This is test 1.6.5 """
#         readCustomer = Customer.objects.get(pk=13)
#         readCustomer.IsActivated = True
#         readCustomer.save()
#         errorMessage = "The operation did not impact the correct record!"
#         self.assertEqual(Customer.objects.get(pk=13).IsActivated, True, errorMessage)

#     def test_1_6_6(self):
#         """ This is test 1.6.6 """
#         with self.assertRaises(Exception):
#             readCustomer = Customer.objects.get(pk=9999)
#             readCustomer.IsActivated = True
#             readCustomer.save()
#             self.fail("A non existent user was written to successfully. That's wrong!")

#     def test_1_6_8(self):
#         """ This is test 1.6.8 """
#         readCustomers = Customer.objects.filter(DateOfBirth = datetime.date(1970, 1, 1))
#         deleteCustomer = readCustomers[1] # Jane Doe
#         CustomerID = deleteCustomer.pk
#         deleteCustomer.delete()
#         with self.assertRaises(Customer.DoesNotExist): 
#             Customer.objects.get(pk=CustomerID)

#     def test_1_6_9(self):
#         """ This is test 1.6.9 """
#         with self.assertRaises(Exception):
#             readCustomer = Customer.objects.get(pk=9999)
#             readCustomer.delete()
#             self.fail("A non existent user was deleted successfully. That's wrong!")
#
# class unit_2_Tests(TestCase):
#     def test_2_1_1(self):
#         """ This is test 2.1.1"""
#         password = b"r3allySecur3"
#         salt = b"$2b$12$Mr8cYTjur7w4gUtGG.P7Mu"
#         expectedHash = b"$2b$12$Mr8cYTjur7w4gUtGG.P7Mu6yHhhj7Vvc/ticID9PZXlY4GmCwfqRe"
#         generatedHash = bcrypt.hashpw(password, salt)
#         self.assertEqual(generatedHash, expectedHash, "The hashes do not match!")
#
#     def test_2_2_1(self):
#         """ This is test 2.2.1 """
#         password = b"r3allySecur3"
#         salt = b"$2b$12$Mr8cYTjur7w4gUtGG.P7Mu"
#         expectedHash = b"$2b$12$Mr8cYTjur7w4gUtGG.P7Mu6yHhhj7Vvc/ticID9PZXlY4GmCwfqRe"
#         generatedHash1 = bcrypt.hashpw(password, salt)
#         generatedHash2 = bcrypt.hashpw(password, salt)
#         condition1 = generatedHash1 == expectedHash
#         condition2 = generatedHash2 == expectedHash
#         if condition1 == False or condition2 == False:
#             self.fail("The hashing algorithm isn't consistent!")
