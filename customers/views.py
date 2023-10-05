from rest_framework import generics

from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class CustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()