from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    signature = models.ImageField(upload_to='signatures/')


class Organization(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    contacts = models.TextField()
    stamp = models.ImageField(upload_to='stamps/')


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    article = models.CharField(max_length=50)
    tags = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='products/')


class CommercialOffer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    number = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='OfferProduct')
    recipient = models.TextField(blank=True, null=True)
    delivery_time = models.CharField(max_length=200)
    decoration = models.CharField(max_length=50, blank=True, null=True)


class OfferProduct(models.Model):
    offer = models.ForeignKey(CommercialOffer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Decoration(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='decorations/')
