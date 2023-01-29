from django.test import TestCase, Client
from django.contrib.auth.models import User
from paymentapp.models import Account
# from paymentapp.views import user_deposit_money, check_balance, user_send_money
from django.urls import reverse

class AccountTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        #create an account for the user
        self.account = Account.objects.create(user=self.user, balance=0)
        
        # Create a client to handle authentication
        self.client = Client()

    def test_user_deposit_money_with_authentication(self):
        # Log in the test user
        self.client.login(username=self.username, password=self.password)

        # Call the function to deposit money to account
        response = self.client.post(reverse('user_deposit_money'), {'amount': 100})
        
        # Check the status code of the response
        self.assertEqual(response.status_code, 201)
        
        # Check that the balance has been updated
        self.assertEqual(Account.objects.get(user=self.user).balance, 100)

    
    def test_user_send_money_with_authentication(self):
        # Log in the test user1
        self.client.login(username=self.username1, password=self.password1)

        # Call the function to send money to user2
        response = self.client.post(reverse('user_send_money'), {'username':self.username2, 'amount': 100})
        
        # Check the status code of the response
        self.assertEqual(response.status_code, 201)
        
        # Check that the balance of user1 has been updated
        self.assertEqual(Account.objects.get(user=self.user1).balance, 900)
        # Check that the balance of user2 has been updated
        self.assertEqual(Account.objects.get(user=self.user2).balance, 100)


    def test_check_balance_with_authentication(self):
        # Log in the test user
        self.client.login(username=self.username, password=self.password)

        # Call the function to check balance
        response = self.client.get(reverse('check_balance'))
        
        # Check the status code of the response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the correct balance
        self.assertContains(response, '1000')

        
    def test_check_balance_without_authentication(self):
        # Call the function to check balance without logging in
        response = self.client.get(reverse('check_balance'))
        
        # Check the status code of the response
        self.assertEqual(response.status_code, 302)
        
        # Check that the user is redirected to the login page
        self.assertRedirects(response, '/login?next=' + reverse('check_balance'))


    def test_transfer_money(self):
        # log in the test user
        self.client.login(username=self.username, password=self.password)
        
        # make a transfer request
        amount = 500.00
        response = self.client.post('/transfer/', {'amount': amount})
        
        # check that the response is successful
        self.assertEqual(response.status_code, 200)
        
        # check that the account's balance has been updated
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 500.00)



