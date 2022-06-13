from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CarBrand(models.Model):
    """class made for car brands"""
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class CarCategory(models.Model):
    """class made fo car categories like econimic,SUV,sport etc."""
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class CarModel(models.Model):
    """Car models for example Opel "Astra" economic """
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    car_category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    capacity = models.IntegerField(default=4)
    picture = models.ImageField(default=False, upload_to='viewer/picture', null=True)

    def __str__(self):
        return f'{self.car_category.name} {self.car_brand.name} {self.name} {self.capacity} osobowy'


class Rental(models.Model):
    """Informations about car rental facility"""
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=120)
    number_of_cars = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Car(models.Model):
    """Every information about one car. What it has and where is it located"""
    TRANSMISSION = [
        ('Manualna', 'Manualna'),
        ('Automat', 'Automat')
    ]

    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    transmission = models.CharField(max_length=30, choices=TRANSMISSION, default=TRANSMISSION[0])
    air_conditioning = models.BooleanField()
    price_per_day = models.FloatField()
    avability = models.BooleanField()

    class Meta:
        permissions = [
            ('rzym_view_car', 'rzym car view'),
            ('londyn_view_car', 'londyn car view'),
            ('paryz_view_car', 'paryz car view'),
        ]

    def __str__(self):
        return f'{self.car_model}'


class Client(models.Model):
    """Client informations"""
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    document_id = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    def __str__(self):
        return f'{self.name} {self.surname}'


class DriverLicense(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=30)


class Booking(models.Model):
    """Relations between client and a car that is desired for reservation"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=None)
    date_of_rental = models.DateField()
    date_of_return = models.DateField()
    number_of_days = models.IntegerField()
    days_to_return = models.IntegerField()
    penalties = models.BooleanField(default=False)
    amount_of_penalties = models.FloatField(default=0)
    insurance = models.BooleanField()
    total_cost = models.FloatField()

    def __str__(self): \
            return f'{self.user} has booked the {self.car} from {self.date_of_rental} ' \
                   f'to {self.date_of_return}'


class Employee(models.Model):
    """An employee that is assigned to one specific rental"""
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Post(models.Model):
    name = models.CharField(max_length=50)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=None)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class ClientTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


