from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50)

class WebsiteColor(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    website = models.CharField(max_length=200)
    color = models.CharField(max_length=7)  # Hex color code
    percentage = models.FloatField(default=0)
