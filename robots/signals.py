from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.services import send_mail_to_customers
from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def post_save_robot(**kwargs):
    new_robot = kwargs.get('instance')
    orders_in_wait = Order.objects.filter(in_stock=False, robot_serial=new_robot.serial)

    if orders_in_wait.exists():
        customers_in_wait = set()
        for order in orders_in_wait:
            customer_email = order.customer.email
            customers_in_wait.add(customer_email)
            order.in_stock = True
            order.save()
        mail_subject = 'Модель в наличии'
        mail_body = f'Добрый день!\n' \
                    f'Недавно вы интересовались нашим роботом модели {new_robot.model}, версии {new_robot.version}.\n' \
                    f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        send_mail_to_customers(subject=mail_subject, body=mail_body, customers_list=customers_in_wait)
