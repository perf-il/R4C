from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from orders.models import Order


class OrdersTest(APITestCase):

    def setUp(self) -> None:
        self.customer = Customer.objects.create(
            email='test@example.com',
        )

    def test_create_order(self):
        """Тестирование создания нового заказа"""
        data = {
            'customer': self.customer.pk,
            'robot_serial': 'R2-D2'
        }

        response = self.client.post(
            reverse('orders:order-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(Order.objects.all().exists())

        self.assertEqual(
                response.json(),
                {
                    'id': 1,
                    'customer': self.customer.pk,
                    'robot_serial': 'R2-D2',
                    'in_stock': False
                }
            )
