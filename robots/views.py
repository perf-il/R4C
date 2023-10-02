from django.shortcuts import render
from rest_framework import generics

from robots.models import Robot
from robots.serializers import RobotSerializer


class RobotCreateAPIView(generics.CreateAPIView):
    serializer_class = RobotSerializer


class RobotListAPIView(generics.ListAPIView):
    serializer_class = RobotSerializer
    queryset = Robot.objects.all()
