from django.shortcuts import render
from .serializers import ListingSerial , BookingSerial ,Paymentserial
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Listing , Booking ,Payment
from .paginations import LargeResultsSetPagination
from rest_framework.response import Response
from rest_framework.decorators import permission_classes , api_view
from .tasks import send_booking_confirmation_email

# Create your views here.

from .chapa import Chapa


class ListingViewset(ModelViewSet):
    serializer_class = ListingSerial
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print(user.username)
        listings = Listing.objects.filter(host_id = user.pk).select_related("host_id") .order_by("-created_at") 
        
        return listings
    
class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerial
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]


    
    
    def get_queryset(self):
        
        
        userbookings = Booking.objects.filter(user_id = self.request.user).select_related("user_id" , "property_id").order_by("-created_at") 
       
        return userbookings
    
    def perform_create(self, serializer):
        print(self.request.user)
        booking = serializer.save()
        user_email = "matrixauto7@gmail.com"
        booking_details = f"Booking ID: {booking.id}\nDestination: {booking.destination}\nDate: {booking.date}"
        
        send_booking_confirmation_email.delay(user_email , booking_details)
        #return super().perform_create(serializer)
    
    
    
    
    
    


class PaymentViewset(ModelViewSet):
    serializer_class = Paymentserial
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    
    def get_queryset(self):
        user = self.request.user
        
        query = Payment.objects.filter(user_id= user.pk).select_related("booking_id")
        return query


@api_view(["POST"])   
@permission_classes([IsAuthenticated])
def makepayment(req , booking_id) :
    user = req.user
   
    try:
        booking = Booking.objects.get(pk = booking_id)
        
    except Booking.DoesNotExist:
        return Response ({"Status":"Failed","data":"Booking Details Does Not Exists"} , status= status.HTTP_404_NOT_FOUND)
    else:
        
        payment = Chapa()
        make_payment = payment.makePayment(user, booking)

        Payment.objects.create(
            booking_id = booking,
            tx_id = make_payment["tx_ref"] ,
            status = "Pending",
            user_id = user,
            amount = booking.property_id.pricepernight
        )

        return Response(make_payment, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])

def verifypayment(req , tx_ref):
    chapa = Chapa()
    verified = chapa.verifypayment(tx_ref)
    
    if verified["status"] != "success" or "data" not in list(verified.keys()):
        return Response ({"Data":"Not Found"} , status=status.HTTP_400_BAD_REQUEST)
    
    payment_status = verified["data"].get("status")
    
    if not payment_status:
           return Response ({"Data":"Payment Status Not Found"} , status=status.HTTP_404_NOT_FOUND)
        
    try:
        payment = Payment.objects.get(tx_id = tx_ref)
          #update the status in the payment database
        payment.status = payment_status.title()

        payment.save()
  
    except Payment.DoesNotExist:
        return Response({"data":"Payment Data not found"} , status=status.HTTP_404_NOT_FOUND)

        
    
    #booking = Booking.objects.get(pk = payment.booking_id.pk)
    
    booking = payment.booking_id
    
    if booking and payment_status == "Success":  
        booking.status = "Confirmed"
        booking.save()    
    
    return Response(verified , status=status.HTTP_200_OK)