from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer


class CustomersTest(APITestCase):

    def test_create_customer(self):
        """Тестирование создания нового клиента"""
        data = {
            'email': 'test-post@example.com',
        }

        response = self.client.post(
            reverse('customers:customer-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(Customer.objects.all().exists())

        self.assertEqual(
                response.json(),
                {
                    'id': 1,
                    'email': 'test-post@example.com'
                }
            )

    def test_list_customer(self):
        """Тестирование списка клиентов"""

        Customer.objects.create(
            email='test-get@example.com',
        )

        response = self.client.get(
            reverse('customers:customers-all')

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [
                {
                    'id': 2,
                    'email': 'test-get@example.com'
                }
            ]
        )

    def test_validations_customer(self):
        """Тестирование валидации полей при добавлении заказчика"""

        Customer.objects.create(
            email='test@example.com',
        )

        data_bad_email = {
            'email': 'bad_email'
        }
        data_not_uniq = {
            'email': 'test@example.com'
        }

        response = self.client.post(
            reverse('customers:customer-create'),
            data=data_bad_email
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            *response.json()['non_field_errors'],
            'Enter a valid email address.'
        )

        response = self.client.post(
            reverse('customers:customer-create'),
            data=data_not_uniq
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            *response.json()['non_field_errors'],
            'Адрес уже зарегистрирован'
        )
