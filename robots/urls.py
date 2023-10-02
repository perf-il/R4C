from django.urls import path

from robots.apps import RobotsConfig
from robots.views import RobotCreateAPIView, RobotListAPIView

app_name = RobotsConfig.name

urlpatterns = [
    path('robot/create/', RobotCreateAPIView.as_view(), name='robot-create'),
    path('all/', RobotListAPIView.as_view(), name='robots-all'),

]