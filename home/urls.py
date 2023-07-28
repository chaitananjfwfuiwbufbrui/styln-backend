from django.urls import path
from .views import SaloonListCreateView, SaloonDetailView, ServicesAPI, PortfolioAPI, TimeSlotAPI

urlpatterns = [
    path('saloon/', SaloonListCreateView.as_view(), name='saloon-list-create'),
    path('saloon/<int:pk>/', SaloonDetailView.as_view(), name='saloon-detail'),
    path('saloon/<int:id>/services/', ServicesAPI.as_view(), name='saloon-services'),
    path('saloon/<int:id>/portfolio/', PortfolioAPI.as_view(), name='saloon-portfolio'),
    path('saloon/<int:id>/time_slot/', TimeSlotAPI.as_view(), name='saloon-time-slot'),
]
