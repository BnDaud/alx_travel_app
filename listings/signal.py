from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from .tasks import sendPaymentmail

@receiver(post_save , sender = Payment)
def paymentInitailization(sender , instance , created , **kwargs):
    
    user = instance.user_id
    
    message = f"""Hi {user.username} ,\n\n
    
    A payment has being initiated in our app with your email {user.email} \n
    Amount  : {instance.amount}\n
    Transaction ID : {instance.tx_id}\n
    Booking : {instance.booking_id.property_id.name}
    """
    
     
    
    if created:
       
        
        sendPaymentmail.delay(to_email=user.email , subject="Payment Initalization" ,message= message )
       
