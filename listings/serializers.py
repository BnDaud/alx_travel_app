from rest_framework import serializers
from .models import User , Listing ,Review ,Booking , Payment
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

class UserSerial(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length = 100 , write_only = True)
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password":{"write_only":True}}
        
        
    def create(self, validated_data):
        pword = validated_data.pop("password")
        cpword = validated_data.pop("confirm_password")
        if cpword != pword:
            raise ValidationError("password not the same")
        
        validated_data["password"] = make_password(pword)
        
        
        
        return super().create(validated_data)
    
    

class ListingSerial(serializers.ModelSerializer):
    host_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = "__all__"
        
    
    def get_host_name(self , obj):
        
        return obj.host_id.username 
    
    

class BookingSerial(serializers.ModelSerializer):
    guest_name = serializers.SerializerMethodField()
    property = ListingSerial(read_only = True , source = "property_id")
    class Meta:
        model = Booking
        fields = "__all__"
        
    
    def get_guest_name(self , obj):
        
        return obj.user_id.username
        
        

class ReviewSerial(serializers.ModelSerializer):
    
    property_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = "__all__"
        
        
    def get_property_name(self , obj):
        return obj.property_id.name
    


class Paymentserial(serializers.ModelSerializer):
    property_name = serializers.SerializerMethodField()
    
    class Meta:
        model= Payment
        fields = "__all__"
        
    
    def get_property_name(self , obj):
       return  obj.booking_id.property_id.name