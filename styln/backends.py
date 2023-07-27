# backends.py

from django.contrib.auth import get_user_model
from django.db.models import Q
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class OTPAuthenticationBackend:
    def authenticate(self, request, email=None, otp=None):
        if email is None or otp is None:
            return None

        User = get_user_model()
        user = None

        # Find the user based on the provided email and OTP
        try:
            user = User.objects.get(
                Q(email__iexact=email),
                Q(otp=otp),
                Q(otp_expiry__gte=datetime.now())
            )
        except User.DoesNotExist:
            return None

        # If OTP verification is successful, set phone_number_verified to True
        user.phone_number_verified = True
        user.save()

        return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
