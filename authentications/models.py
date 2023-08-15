from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
import random

def unique_usernumber(instance, new_id=None):
    ct = datetime.datetime.now().date()
    number = 1
    if new_id is not None:
        id = new_id
    else:
        id = 'f' + str(ct) + str(number)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=id).exists()
    if qs_exists:
        new_id = "f{date}{idgen}{rand}".format(
            date=ct,
            idgen=number + 1,
            rand=random.randrange(0, 100000),
        )
        return unique_usernumber(instance, new_id=new_id)

    return id


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


ACCOUNT_TYPE_CHOICES = (
    ("CONSULTANT", "Consultant"),
    ("HR", "HR"),
    ("ACCOUNTANT", "Accountant"),
    ("PROJECT MANAGER", "Project Manager"),
)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=255, default="S", unique=True)
    email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255,default = "S")
    # last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    type_of_account = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='CONSULTANT'
    )
    
    phone_number = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=200,default = "-")
    state = models.CharField(max_length=200,default = "-")
    latitude = models.CharField(max_length=200,default = "-")
    longitude = models.CharField(max_length=200,default = "-")
    otp = models.CharField(max_length=6, blank=True, null=True,default= '100')  # Add the otp field
    phone_number_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user/profile',default = "https://cdn-icons-png.flaticon.com/512/219/219988.png")
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',  'phone_number','city','state']

    # Method to generate and save OTP to the user
    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp = otp
        # Set OTP expiration (e.g., 5 minutes from now)
        self.otp_expiry = timezone.now() + datetime.timedelta(minutes=5)
        self.save()
    def get_full_name(self):
        return f"{self.user_name}"

    def get_short_name(self):
        return self.user_name
    
    def __str__(self):
        return self.email


def user_number_generator(sender, instance, *args, **kwargs):
    if instance.user_id:
        instance.user_id = unique_usernumber(instance)

pre_save.connect(user_number_generator, sender=UserAccount)
