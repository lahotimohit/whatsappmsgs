from django.db import models

# Create your models here.
class UserData(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name