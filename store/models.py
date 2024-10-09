import os

from typing import Optional
from django.db import models
from djangoProject.settings import MEDIA_URL


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
    price = models.DecimalField(verbose_name='ფასი', max_digits=10, decimal_places=2)
    category = models.ManyToManyField(
        to='Category', verbose_name='კატეგორიები',
    )
    product_add_date = models.DateTimeField(auto_now_add=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(verbose_name='პროდუქტის ფოტო', upload_to='store/', blank=True)
    rating = models.IntegerField(default=5, verbose_name='პროდუქტის რეიტინგი')

    class Meta:
        ordering = ['-id']

    def values(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description ,
            'price': float(self.price),
            'slug': self.slug,
            'categories': [
                cat.values(include_parent=False) for cat in self.category.all()
            ],
            'create_time': self.product_add_date,
            'last_mod': self.last_modify_date,
            'image': MEDIA_URL + self.image.name if self.image else None,
            'rating': self.rating
        }

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):  # წავშალოთ ფოტო ობიექტის წაშლისას
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
