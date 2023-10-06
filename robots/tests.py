import re

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from robots.models import Robot


class RobotsTest(APITestCase):

    def test_create_robot(self):
        """Тестирование создания нового робота"""
        data = {
            'model': 'R2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59',
        }

        response = self.client.post(
            reverse('robots:robot-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(Robot.objects.all().exists())

        self.assertEqual(
                response.json(),
                {
                    'id': 1,
                    'serial': 'R2-D2',
                    'model': 'R2',
                    'version': 'D2',
                    'created': '2022-12-31T23:59:59Z'
                }
            )

    def test_list_customer(self):
        """Тестирование списка роботов"""

        Robot.objects.create(
            model='R2',
            version='D2',
            created='2022-12-31 23:59:59',
        )

        response = self.client.get(
            reverse('robots:robots-all')

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
                    'serial': 'R2-D2',
                    'model': 'R2',
                    'version': 'D2',
                    'created': '2022-12-31T23:59:59Z'
                }
            ]
        )

    def test_validations_robot(self):
        """Тестирование валидации полей при добавлении робота"""

        data_bad_model = {
            'model': 'R',
            'version': 'D2',
            'created': '2022-12-31T23:59:59Z',

        }

        data_bad_version = {
            'model': 'R2',
            'version': 'D',
            'created': '2022-12-31T23:59:59Z',

        }

        data_bad_created = {
            'model': 'R2',
            'version': 'D2',
            'created': '2025-12-31T23:59:59Z',

        }

        response = self.client.post(
            reverse('robots:robot-create'),
            data=data_bad_model
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            *response.json()['non_field_errors'],
            f"Модель должна быть выражена двух-символьной последовательностью(например R2)"
        )

        response = self.client.post(
            reverse('robots:robot-create'),
            data=data_bad_version
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            *response.json()['non_field_errors'],
            f"Версия должна быть выражена двух-символьной последовательностью(например 11)"
        )

        response = self.client.post(
            reverse('robots:robot-create'),
            data=data_bad_created
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            *response.json()['non_field_errors'],
            f"Нельзя указать будущее время"
        )

        self.assertFalse(
            Robot.objects.all().exists()
        )

    def test_get_report(self):
        """Тестирование запроса на создание отчета"""

        response = self.client.get(
            reverse('robots:export-data')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.headers.get('Content-Type'),
            'application/vnd.ms-excel'
        )

        self.assertTrue(
            bool(re.search(r'attachment; filename="report_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.xls"',
                           response.headers.get('Content-Disposition')))
        )
