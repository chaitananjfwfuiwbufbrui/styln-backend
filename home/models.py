from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Saloon(models.Model):
    # Attributes of the salon
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    distance = models.CharField(max_length=15)
    rating = models.FloatField()
    is_ac = models.BooleanField(default=False)
    image = models.ImageField(upload_to='saloon_images/')
    facilities = models.TextField()  # This will be stored as a comma-separated list

    # Contact details
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.CharField(max_length=100)
    
    # Timings of the salon
    timings = models.CharField(max_length=100)

    # Additional fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    available_for = models.TextField()  # Storing as a JSON array
    sallon_staff = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

class Service(models.Model):
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    TYPES = (
        ('beard', 'Beard'),
        ('hair', 'Hair'),
    )
    typeofserv = models.CharField(choices=TYPES, max_length=5)
    prize = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    image = models.ImageField(upload_to=None,default = "dsds")

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    time = models.TimeField()
    comment = models.TextField()
    image = models.ImageField(upload_to=None)

    def __str__(self):
        return self.name

class Time_slot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='barber_portfolio')
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    dateandtime = models.DateTimeField()
    slot_status = models.BooleanField()
    
    def __str__(self):
        return f"{self.user.user_name}'s Portfolio {self.id}"
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    slot = models.ForeignKey(Time_slot, on_delete=models.CASCADE)
    dateandtime = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s booking on {self.dateandtime}"

