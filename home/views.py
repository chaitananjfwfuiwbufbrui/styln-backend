from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Saloon, Service, Portfolio, Time_slot
from .serializers import SaloonSerializer, SaloonSIngle_Serializer, ServiceSerializer, PortfolioSerializer, Time_slotSerializer
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
class Lcation_taker(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get(self, request, id):
        user = request.user
        user.latitude = request.get.data('latitude')
        user.longitude = request.get.data('longitude')
        user.save()

        message = {"message": "location  saved"}
        return JsonResponse(message, status=status.HTTP_200_OK)
class Lcation_taker(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get(self, request, id):
        user = request.user
        user.latitude = request.get.data('latitude')
        user.longitude = request.get.data('longitude')
        user.save()

        message = {"message": "location  saved"}
        return JsonResponse(message, status=status.HTTP_200_OK)
