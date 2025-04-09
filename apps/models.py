from django.db import models
from django.db.models import Model, DecimalField, ForeignKey, SET_NULL, DateTimeField, CASCADE, TextChoices

from authentication.models import User


# Create your models here.
class Order(Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    stadium = ForeignKey('Stadium', on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    start_time = DateTimeField(null=True, blank=True)
    end_time = DateTimeField(null=True, blank=True)


class Stadium(Model):
    class RegionChoices(TextChoices):
        yunusobod='yunusobod','Yunusobod'
        chilonzor='chilonzor','Chilonzor'
        olmazor='olmazor','Olmazor'
        sergeli='sergeli','Sergeli'
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255,choices=RegionChoices.choices)
    location_note = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_stadiums')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='manager_stadiums',null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)


class PlatformStadium(Model):
    stadium = ForeignKey(Stadium, on_delete=CASCADE, null=True)
