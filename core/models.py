
from django.db import models


class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Produce(models.Model):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name="produce"
    )
    crop_name = models.CharField(max_length=100)
    quantity_kg = models.FloatField()
    price_per_kg = models.FloatField()
    harvest_date = models.DateField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.crop_name} - {self.farmer.name}"


class BuyerOrder(models.Model):
    buyer_name = models.CharField(max_length=100)
    crop_name = models.CharField(max_length=100)
    required_quantity_kg = models.FloatField()
    target_price_per_kg = models.FloatField()
    delivery_location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.buyer_name}"

