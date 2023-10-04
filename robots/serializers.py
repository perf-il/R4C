from django.utils import timezone
from rest_framework import serializers

from robots.models import Robot


class RobotSerializer(serializers.ModelSerializer):

    serial = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Robot
        fields = '__all__'

    def validate(self, data):

        if len(data.get('model')) != 2:
            raise serializers.ValidationError(
                'Модель должна быть выражена двух-символьной последовательностью(например R2)')

        if len(data.get('version')) != 2:
            raise serializers.ValidationError(
                'Версия должна быть выражена двух-символьной последовательностью(например 11)')

        if data.get('created') >= timezone.now():
            raise serializers.ValidationError('Нельзя указать будущее время')

        return data

    def get_serial(self, instance):
        self.serial = f'{instance.model}-{instance.version}'
        return self.serial
