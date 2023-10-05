from django.urls import path

from customers.apps import CustomersConfig
from customers.views import CustomerCreateAPIView, CustomerListAPIView

app_name = CustomersConfig.name

urlpatterns = [
    path('customer/create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('all/', CustomerListAPIView.as_view(), name='customers-all'),

]
