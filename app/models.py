from django.db import models
from django.contrib.auth.models import User

class ComputerConfig(models.Model):
    config = models.JSONField()
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.address

class PreRegistration(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    otp = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"PreRegistration for {self.user.username}"

