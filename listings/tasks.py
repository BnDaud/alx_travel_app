from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def sendPaymentmail(to_email , subject , message):
    
    send_mail(
        subject=subject,
        message= message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False
    ) 
 
 
    
@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Dear Customer,\n\nYour booking has been confirmed.\n\nDetails:\n{booking_details}\n\nThank you for using our service!"
    
    send_mail(
        subject ,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )
    return f"Email sent to {user_email}"