

from django.db import models, transaction

class Website(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url

class FontSize(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    font_size = models.CharField(max_length=500)

    def __str__(self):
        return self.font_size



class ArrayModel(models.Model):
    data = models.TextField()


    def delete(self, *args, **kwargs):
        with transaction.atomic():
            super().delete(*args, **kwargs)
            # Check if this is the last row
            if ArrayModel.objects.count() == 0:
                # Reset auto-increment counter for the primary key
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE myapp_mymodel AUTO_INCREMENT = 1;")


