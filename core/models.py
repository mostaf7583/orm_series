from django.db import models

# Create your models here.
class Resturant(models.Model):
    name = models.char
    website
    latitude
    longitude
    restaurant_type

    def __str__ (self):
        return self.name

