from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order Summary'
    message = f'Dear {order.first_name},\n\n' \
        f'Your order has been successfully placed.'
    mail_sent = send_mail(subject, message, 'admin@fooddeli.com', [order.email])
    return mail_sent
