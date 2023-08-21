from rest_framework import generics, permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import SaloonSerializer, BookingSerializer,SaloonSIngle_Serializer, ServiceSerializer, PortfolioSerializer, Time_slotSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser  # Add this import line
from styln.settings import AUTH_USER_MODEL
class SaloonListCreateView(generics.ListCreateAPIView):
    queryset = Saloon.objects.all()
    serializer_class = SaloonSerializer
    permission_classes = [permissions.IsAuthenticated]

class SaloonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Saloon.objects.all()
    serializer_class = SaloonSIngle_Serializer
    permission_classes = [permissions.IsAuthenticated]

class ServicesAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get(self, request, id):
        saloon = Saloon.objects.get(id=id)
        services = Service.objects.filter(saloon=saloon)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class PortfolioAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get(self, request, id):
        saloon = Saloon.objects.get(id=id)
        portfolios = Portfolio.objects.filter(saloon=saloon)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

class TimeSlotAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get(self, request, id):
        saloon = Saloon.objects.get(id=id)
        time_slots = Time_slot.objects.filter(saloon=saloon)
        serializer = Time_slotSerializer(time_slots, many=True)
        return Response(serializer.data)

class LocationTaker(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def post(self, request):
        try:
            user = request.user
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            
            if latitude is None or longitude is None:
                return Response({"error": "Latitude and longitude must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.latitude = latitude
            user.longitude = longitude
            user.save()

            message = {"message": "Location saved"}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Booking_view(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def post(self, request, pid):
        try:
            time = Time_slot.objects.get(id=pid)
            if   time.slot_status:
                time.slot_status = True
                time.user = request.user
                time.save()
                bok, created = Booking.objects.get_or_create(user=request.user, slot=time)
                
                # Use your serializer to serialize the booking instance
                ser = BookingSerializer(bok)
                
                message = {"message": "Booking saved" if created else "Booking already exists"}
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Time slot has booked."}, status=status.HTTP_404_NOT_FOUND)

            
        except Time_slot.DoesNotExist:
            return Response({"error": "Time slot does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)