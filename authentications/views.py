from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random
from django.views import View
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAccount

# Helper function to send OTP via email
def send_otp(email):
    User = get_user_model()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Save the OTP to the user object
    user.otp = otp
    user.save()

    # Replace 'YOUR_EMAIL_HOST_USER' with your email host user
    # and update the subject and message as needed.
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'

    # Send the OTP via email
    send_mail(subject, message, 'YOUR_EMAIL_HOST_USER', [email], fail_silently=False)

    return otp

# API View for OTP verification
class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.otp == otp:
            # If OTP verification is successful, set phone_number_verified to True
            user.phone_number_verified = True
            user.otp = None
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)

            # return Response({'detail': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)

# API View to send OTP via email
class OTPLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        otp = send_otp(email)

        if otp:
            return Response({'detail': 'OTP sent'})
        else:
            return Response({'detail': 'Email not registered'}, status=status.HTTP_400_BAD_REQUEST)

# API View for creating a superuser account
class SuperUserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Assuming UserAccount is the custom user model
        us = request.user
        us.is_staff = True
        us.is_superuser = True
        us.save()
        message = {"message": "Superuser created"}
        return JsonResponse(message, status=status.HTTP_200_OK)

# API View for phone number JWT authentication
class PhoneJWTAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')

        try:
            user = UserAccount.objects.get(phone_number=phone_number)
        except UserAccount.DoesNotExist:
            return Response({'detail': 'Phone number not registered'}, status=status.HTTP_401_UNAUTHORIZED)

        # If phone number exists, create and return JWT token
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
