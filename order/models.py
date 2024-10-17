from django.db import models
from user.models import User


class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="მომხმარებელი")

    def __str__(self):
        return f"{self.user.username}'s cart"
