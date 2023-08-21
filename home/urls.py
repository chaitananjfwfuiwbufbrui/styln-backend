from django.urls import path
from .views import *

urlpatterns = [
    path('saloon/', SaloonListCreateView.as_view(), name='saloon-list-create'),
    path('Location_taker/', LocationTaker.as_view(), name='LocationTaker'),
    path('booking/<int:pid>/', Booking_view.as_view(), name='Booking'),
    path('saloon/<int:pk>/', SaloonDetailView.as_view(), name='saloon-detail'),
    path('saloon/<int:id>/services/', ServicesAPI.as_view(), name='saloon-services'),
    path('saloon/<int:id>/portfolio/', PortfolioAPI.as_view(), name='saloon-portfolio'),
    path('saloon/<int:id>/time_slot/', TimeSlotAPI.as_view(), name='saloon-time-slot'),
]
