from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)


class ProductCategory(models.Model):
    category = models.CharField(max_length=64, default=None)


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    price = models.FloatField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="./images")
    thumbnail = models.ImageField(upload_to="./thumbnails")


class Address(models.Model):
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=32)
    street = models.CharField(max_length=128)
    building_number = models.CharField(max_length=32)
    apartament_number = models.IntegerField(default=None)


class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    ordered_products_summary = models.JSONField()
    order_date = models.DateField()
    payment_date = models.DateField()
    price = models.FloatField()
