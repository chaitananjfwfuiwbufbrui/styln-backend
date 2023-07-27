
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random

def send_otp(email):
    User = get_user_model()
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return "Mail not registered"

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

    return "OTP sent"
