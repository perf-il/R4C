import os

from django.conf.urls.static import static
from django.urls import path

from R4C import settings
from robots.apps import RobotsConfig
from robots.views import RobotCreateAPIView, RobotListAPIView, export_data, download_view_test

app_name = RobotsConfig.name

urlpatterns = [
    path('robot/create/', RobotCreateAPIView.as_view(), name='robot-create'),
    path('all/', RobotListAPIView.as_view(), name='robots-all'),
    path('export-data/', export_data, name='export-data'),
    path('download-test/', download_view_test, name='download-test'),

] + static('/reports/', document_root=os.path.join(settings.BASE_DIR, 'reports'))
