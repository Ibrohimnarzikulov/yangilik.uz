from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass









class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars',null=True, blank=True)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.user.username