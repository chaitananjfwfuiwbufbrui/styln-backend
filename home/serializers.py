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
        # fields = ['name','prize','barber_detailes','distance','rating','is_ac','image','facilities','phone','email','website','timings','available_for','sallon_staff']
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class Time_slotSerializer(serializers.ModelSerializer):
    barber_detailes = serializers.SerializerMethodField('get_barber_details')

    def get_barber_details(self, obj):
        barber_details = obj.saloon  # Assuming 'barber' is a ForeignKey field in Time_slot
        serializer = SaloonSerializer(barber_details)
        return serializer.data

    class Meta:
        model = Time_slot
        fields = ["user", "barber", "saloon", "service", "dateandtime", "slot_status", "barber_detailes"]

class BookingSerializer(serializers.ModelSerializer):
    slot_det = serializers.SerializerMethodField('get_slot_details')

    def get_slot_details(self, obj):
        slot_details = Time_slot.objects.filter(id=obj.slot.id).first()
        if slot_details:
            serializer = Time_slotSerializer(slot_details)
            return serializer.data
        return None

    class Meta:
        model = Booking
        fields = ['slot', 'slot_det', 'payment_status', 'dateandtime', 'payment_id']