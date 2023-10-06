from datetime import timedelta

import xlwt
from django.db.models import Count

from django.utils import timezone

from robots.models import Robot


def report_save_excel(days=7):
    """
    Функция для формирования файла в формате .xls
    со сводкой по суммарным показателям производства роботов (модель - Robot)
    :param days: кол-во дней, за которые будет сформирован отчет (по-умолчанию 7 дней)
    :return: строку с именем файла
    """
    style0 = xlwt.easyxf('font: name Times New Roman, bold on', num_format_str='#,##0.00')

    all_robots = Robot.objects.all()
    wb = xlwt.Workbook()
    for robot in all_robots.distinct('model'):
        sorted_robots = all_robots.filter(model=robot.model, created__gte=timezone.now() - timedelta(days=days))
        if sorted_robots:
            ws = wb.add_sheet(f'Model-{robot.model}')

            ws.write(0, 0, 'Модель', style0)
            ws.write(0, 1, 'Версия', style0)
            ws.write(0, 2, "Количество за неделю", style0)

            for i, model in enumerate(
                    sorted_robots.values('model', 'version').annotate(dcount=Count('version')).order_by()):
                ws.write(i + 1, 0, model['model'])
                ws.write(i + 1, 1, model['version'])
                ws.write(i + 1, 2, model['dcount'])

    file_name = f'report_{timezone.now().strftime("%Y-%m-%d-%H-%M-%S")}.xls'

    try:
        wb.save(f'reports/{file_name}')
    except IndexError:
        wb.add_sheet('empty_report')
        wb.save(f'reports/{file_name}')

    return file_name
