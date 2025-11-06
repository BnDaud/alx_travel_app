from django.db import models
from uuid import uuid4
from django.contrib.auth.models import  AbstractUser
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.exceptions import ValidationError

def rating_validator(arg):
    if arg < 1 or arg > 5:
        raise ValidationError ("Value should be not be lesser than 1 or greater than 5 ")


class User(AbstractUser):
    id = models.UUIDField(default=uuid4 , primary_key=True , editable=False)
    phone_number = models.CharField(max_length=50 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10 , choices= [("host" ,"host") , ("admin" , "admin") , ("guest" ,"guest")])

class Listing(models.Model):
    
    id = models.UUIDField(primary_key=True , default=uuid4 , editable=False)
    host_id = models.ForeignKey(User , on_delete=models.CASCADE , related_name="Listing")
    name = models.CharField(max_length=200 )
    description = models.TextField(max_length=2000 , blank=False)
    location = models.CharField(max_length=500 , blank=False)
    pricepernight = models.DecimalField(decimal_places= 2 , blank=False ,max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.name

class Booking(models.Model):
    
    class Status(models.TextChoices):
        pending = "Pending" , "Pending"
        confirmed = "Confirmed" , "Confirmed"
        canceled = "Canceled" , "Canceled"
    
    id = models.UUIDField(default=uuid4 , primary_key=True , editable=False )
    property_id = models.ForeignKey(Listing , on_delete=models.CASCADE , related_name="bookings")
    user_id = models.ForeignKey(User , on_delete=models.CASCADE , related_name="bookings")
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank = False)
    total_price = models.DecimalField(max_digits=10 , decimal_places=2 , blank=False)
    status = models.CharField(max_length=25 , choices=Status.choices , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.property_id.name

class Review(models.Model):    
    id = models.UUIDField(default=uuid4 , primary_key=True , editable=False)
    property_id = models.ForeignKey(Listing , on_delete=models.CASCADE , related_name="reviews")
    rating = models.SmallIntegerField(validators=[MinValueValidator(1) , MaxValueValidator(5)])
    comment = models.TextField(max_length=500 , blank=False)
    created_at = models.DateTimeField(auto_now_add=True)   


class Payment(models.Model):
    id = models.UUIDField(default=uuid4 , editable=False , primary_key=True)
    
    booking_id = models.ForeignKey(Booking , on_delete=models.CASCADE , related_name="payments" , blank=False)
    
    user_id = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    
    amount = models.DecimalField(max_digits=10 , decimal_places=2 , blank=False)
    
    tx_id = models.CharField(max_length=50, blank=True , unique=True)
    
    status = models.CharField(max_length=20 , blank=True,choices=(("Pending","Pending") ,("Failed/Cancelled" , "Failed/Cancelled") , ("Success" , "Success")))
    
    
    
    def __str__(self):
        
        return self.booking_id.property_id.name