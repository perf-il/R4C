from rest_framework import generics

from orders.models import Order
from orders.serializers import OrderSerializer
from robots.models import Robot


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        new_order = serializer.save()
        new_order.robot_serial = new_order.robot_serial.upper()
        new_order.in_stock = Robot.objects.filter(serial=new_order.robot_serial).exists()
        new_order.save()


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
