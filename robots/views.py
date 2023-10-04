from django.shortcuts import render
from django.http import FileResponse
from rest_framework.decorators import api_view


from rest_framework import generics

from robots.models import Robot
from robots.serializers import RobotSerializer
from robots.services import report_save_excel


class RobotCreateAPIView(generics.CreateAPIView):
    serializer_class = RobotSerializer

    def perform_create(self, serializer):
        new_robot = serializer.save()
        new_robot.serial = f'{new_robot.model}-{new_robot.version}'
        new_robot.save()


class RobotListAPIView(generics.ListAPIView):
    serializer_class = RobotSerializer
    queryset = Robot.objects.all()


def download_view_test(request):
    """Контроллер для теста работы export_data в браузере"""
    context = {
        'title': 'Тест export_data',
    }
    return render(request, 'robots/download_view_test.html', context)


@api_view(['GET'])
def export_data(request):
    if request.method == 'GET':
        file_name = report_save_excel()
        path = f'reports/{file_name}'
        response = FileResponse(open(path, 'rb'), filename=file_name, as_attachment=True)
        return response
