from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    username = models.CharField(
        max_length=255, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(
        max_length=254, verbose_name="email почта", blank=True)
    phone_number = models.CharField(
        max_length=255, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    facebook = models.URLField("Facebook", default="https://www.facebook.com/")
    twitter = models.URLField("Twitter", default="https://www.twitter.com/")
    linkedin = models.URLField("Linkedin", default="https://www.linkedin.com/")

    def __str__(self):
        return self.username
