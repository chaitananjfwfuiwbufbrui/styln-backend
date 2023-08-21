from rest_framework import serializers
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from django.conf import settings
from authentications.serializers import *
from rest_framework.views import APIView
class SaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = '__all__'
class SaloonSIngle_Serializer(serializers.ModelSerializer):
    barber_detailes = serializers.SerializerMethodField('QUES')
    def QUES(self,obj):
        ques_detailes = obj.sallon_staff.all()
        serializer = UserCreateSerializer(ques_detailes,many = True)
        return serializer.data

    class Meta:
        model = Saloon
        fields = ['name','prize','barber_detailes','distance','rating','is_ac','image','facilities','phone','email','website','timings','available_for','sallon_staff']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
class Time_slotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time_slot
class booking_seralizer(serializers.ModelSerializer):
    slot_det = serializers.SerializerMethodField('slot_query')
    def slot_query(self,obj):
        ques_detailes = Time_slot.object.filter(id = obj.slot.id)
        serializer = UserCreateSerializer(ques_detailes)
        return serializer.data

    class Meta:
        model = Booking
        fields = ['slot','slot_det','payment_status','dateandtime','payment_id',]
        # fields = '__all__'