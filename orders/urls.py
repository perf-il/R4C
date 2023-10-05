from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderCreateAPIView, OrderListAPIView

app_name = OrdersConfig.name

urlpatterns = [
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('all/', OrderListAPIView.as_view(), name='orders-all'),

]
