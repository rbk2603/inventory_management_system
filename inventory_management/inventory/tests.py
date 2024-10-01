from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ItemTests(APITestCase):
    def test_create_item(self):
        response = self.client.post(reverse('item-list'), {'name': 'Test Item', 'description': 'Test Description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    