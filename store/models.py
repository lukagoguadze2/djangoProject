import os

from typing import Optional
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from .managers import CategoryManager, ProductManager


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='კატეგორიის სახელი')
    slug = models.SlugField(max_length=255, blank=True)
    parent = TreeForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='მშობელი კატეგორია',
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ['name']

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @staticmethod
    def __get_name_and_id(category: Optional['Category'] = None) -> dict:
        return {
            'id': category.id,
            'name': category.name
        } if category else None

    def values(self, include_parent: bool = False):
        category = self.__get_name_and_id(self)
        if include_parent:
            category['parent'] = self.__get_name_and_id(self.parent)

        return category

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='პროდუქტის სახელი')
    description = models.TextField(blank=True, verbose_name='პროდუქტის აღწერა', default='')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ფასი')
    quantity = models.IntegerField(default=0, verbose_name='რაოდენობა')
    servings = models.IntegerField(blank=True, default=0, verbose_name='ულუფა')
    preparation_time = models.IntegerField(blank=True, null=True, verbose_name='მომზადების დრო წამებში')
    category = models.ManyToManyField(
        to='Category', verbose_name='კატეგორიები'
    )
    tags = models.ManyToManyField(
        to='Tag', verbose_name='თეგები'
    )
    product_add_date = models.DateTimeField(auto_now_add=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='store/', blank=True, verbose_name='პროდუქტის ფოტო')
    rating = models.IntegerField(default=5, verbose_name='პროდუქტის რეიტინგი')

    class Meta:
        ordering = ['-id']

    objects = ProductManager()

    def values(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'quantity': self.quantity,
            'servings': self.servings,
            'preparation_time': self.preparation_time,
            'slug': self.slug,
            'categories': [
                cat.values(include_parent=False) for cat in self.category.all()
            ],
            'create_time': self.product_add_date,
            'last_mod': self.last_modify_date,
            'image': settings.MEDIA_URL + self.image.name if self.image else None,
            'rating': self.rating,
        }

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):  # წავშალოთ ფოტო ობიექტის წაშლისას
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='თეგის სახელი')

    def __str__(self):
        return self.name
