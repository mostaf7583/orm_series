from django.db import models

# Create your models here.
class Resturant(models.Model):
    class TypeChoices(models.TextChoices):
        INDIAN = 'IN', 'Indian'
        CHINESE = 'CH', 'Chinese'
        ITALIAN = 'IT', 'Italian'
        GREEK = 'GR', 'Greek'
        MEXICAN = 'MX', 'Mexican'
        FASTFOOD = 'FF', 'Fast Food'
        OTHER = 'OT', 'Other'
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    latitude= models.FloatField()
    longitude= models.FloatField()
    type=models.CharField(max_length=2,choices=TypeChoices.choices)
    

    def __str__ (self):
        return self.name
class Rating(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    resturant=models.ForeignKey(Resturant,on_delete=models.CASCADE)
    rating=models.FloatField()
    def __str__(self):
        return f"{self.user.username} - {self.resturant.name} - {self.rating}"

class Sale(models.model):
    resturant=models.ForeignKey(Resturant,on_delete=models.SET_NULL,null=True)
    income=models.DecimalField(max_digits=8,decimal_places=2)


