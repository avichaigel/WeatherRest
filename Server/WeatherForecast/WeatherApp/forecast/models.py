from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=15, blank=False)
    last_lat = models.DecimalField(decimal_places=18, max_digits=25, default="1000.00")
    last_lng = models.DecimalField(decimal_places=18, max_digits=25, default="1000.00")
