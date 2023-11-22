from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=200)

class Items(models.Model):
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Subscription(models.Model):
    subscription_name = models.CharField(max_length=200)
