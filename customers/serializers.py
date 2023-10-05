from rest_framework import serializers

from django.core.validators import validate_email

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self, data):

        validate_email(data.get('email'))

        if Customer.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('Адрес уже зарегистрирован')

        return data
