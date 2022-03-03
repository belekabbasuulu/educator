from django.db import models
from users.models import User


class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return self.title


class Listing(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Categories, verbose_name="Категория", on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Цена")
    description = models.TextField(null=True, verbose_name="Описание")
    listing_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
