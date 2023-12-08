from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    ADMIN = 1
    MODERATOR = 2
    BASIC = 3

    role_choices = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (BASIC, 'Basic'),
    )

    role = models.PositiveSmallIntegerField(choices=role_choices, null=True, blank=True)

    username = None
    date_joined = None
    is_active = None
    is_staff = None
    is_superuser = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    