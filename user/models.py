from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    @staticmethod
    def __validate_fields(email, username, password):
        if not email and not username:
            raise ValueError('შეიყვანეთ იმეილი ან მომხმარებლის სახელი')
        if not password:
            raise ValueError('შეიყვანეთ პაროლი')

    def create_user(self, email='', username='', password=None):
        self.__validate_fields(email, username, password)

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username if username else email.split('@')[0]
        )
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email='', username='', password=None):
        self.__validate_fields(email, username, password)

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="დაბადების თარიღი")
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name="ტელეფონის ნომერი")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="მისამართი")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="ბოლო აქტიურობა")

    objects = UserManager()

    @staticmethod
    def get_absolute_url():
        return reverse('user:login')

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)
