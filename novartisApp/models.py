from django.db import models

# Create your models here.

class ContactBook(models.Model):
    name = models.CharField(max_length=100)
    number = models.ImageField()
    email = models.EmailField()
    address = models.CharField(max_length=200)
