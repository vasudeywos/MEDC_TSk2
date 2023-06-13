import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.status == 'A':
        subject = 'Appointment Approved'
        mainbody = f"Your appointment for {instance.appointment_date} has been approved."
        message=f'Subject: {subject}\n\n{mainbody}'
        from_email = 'devtesting356@gmail.com'
        to_email = instance.patient.email


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
            email_address = 'devtesting356@gmail.com'
            email_password = 'upymnjseoskfsuda'
            connection.login(email_address, email_password)
            connection.sendmail(from_addr=email_address, to_addrs=to_email, msg=message)
            connection.close()
