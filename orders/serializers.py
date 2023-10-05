from rest_framework import serializers

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


class OrderSerializer(serializers.ModelSerializer):

    customer = serializers.SlugRelatedField(slug_field='pk', queryset=Customer.objects.all())
    in_stock = serializers.BooleanField(default=False)

    class Meta:
        model = Order
        fields = '__all__'

    def get_in_stock(self, instance):
        return Robot.objects.filter(serial=instance.robot_serial).exists()
