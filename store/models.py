import os

from django.utils.text import slugify
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='კატეგორიის სახელი')
    parent = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='მშობელი კატეგორია'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='პროდუქტის სახელი')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(verbose_name='ფასი', max_digits=10, decimal_places=2)
    category = models.ManyToManyField(
        to='Category', verbose_name='კატეგორიები',
    )
    product_add_date = models.DateTimeField(auto_now_add=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(verbose_name='პროდუქტის ფოტო', upload_to='store/', blank=True)
    rating = models.IntegerField(default=5, max_length=1)

    class Meta:
        ordering = ['-id']

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
