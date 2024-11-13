from django.db import models

class Website(models.Model):
    url = models.URLField(unique=True)
    font_sizes = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.url
