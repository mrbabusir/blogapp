from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=200,null=True, unique=True,)
    USERNAME_FIELD = "email"  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ["first_name", "last_name","username"]
