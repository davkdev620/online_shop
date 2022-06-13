from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """Task to send an email notification when an order is successfully created."""
    order = Order.objects.get(id=order_id)

    # Create invoice email.
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Pleas, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'YOURMAIL@gmail.com', [order.email])

    # Generate PDF.
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach PDF file.
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # Send email.
    email.send()
