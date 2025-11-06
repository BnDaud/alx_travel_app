from rest_framework.routers import DefaultRouter
from .views import ListingViewset , BookingViewSet , PaymentViewset , makepayment , verifypayment
from django.urls import path

router = DefaultRouter()

router.register("listings", ListingViewset, basename="listings")
router.register("bookings" , BookingViewSet , basename="bookings")
router.register("payments" , PaymentViewset , basename="payments")



urlpatterns = router.urls

new_urls = [
    path("makepayment/<booking_id>" , view=makepayment , name = "makepayment"),
    path("verifypayment/<tx_ref>", view=verifypayment, name="verifypayment")
    ]

urlpatterns.extend( new_urls)