from rest_framework.test import APITestCase

class P2PTestCase(APITestCase):

    def test_add_user(self):
        url = '/users/'
        data = {'name': 'user1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'User added successfully')

    def deposit(self):
        url = '/users/deposit/'
        data = {'name': 'user1', 'amount': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Deposit successful')
