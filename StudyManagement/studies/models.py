from django.db import models

class Study(models.Model):
    name = models.CharField(max_length=100)
    phase = models.CharField(max_length=20)
    sponsor = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Register(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
