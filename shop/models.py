from django.conf import settings
from django.db import models
from django.db.models import ImageField
COLOR_CHOICES = (('red', 'Red color'), ('green', 'Green color'), ('white', 'White color'))


class Product(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=200, choices=COLOR_CHOICES, blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=7)
    image = ImageField(upload_to="products/", blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    external_id = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Product:{self.title}"


class Purchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
