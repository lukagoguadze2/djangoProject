from django.db import models

from user.models import User
from store.models import Product


class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="მომხმარებელი")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="კალათის შექმნის დრო")

    def __str__(self):
        return f"{self.user.username}'s cart"


class Item(models.Model):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, verbose_name="მომხმარებლის კალათა")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="პროდუქტი")
    quantity = models.PositiveIntegerField(default=1, verbose_name="რაოდენობა")

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return self.product.name
