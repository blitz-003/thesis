# palette_analyzer/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Website(models.Model):
    url = models.URLField()
    country = models.CharField(max_length=100)
    palette = ArrayField(ArrayField(models.IntegerField(), size=3), size=10, blank=True, null=True)  # Assuming up to 10 colors

    def __str__(self):
        return self.url
