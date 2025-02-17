from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(
        max_length=50,
        choices=[("Fruit", "Fruit"), ("Vegetable", "Vegetable"), ("Grain", "Grain"), ("Other", "Other")]
    )
    shelf_life_days = models.IntegerField(help_text="Number of days before spoilage",default=10)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    UNIT_CHOICES = [("kg", "Kilogram"), ("ltr", "Liter"), ("unit", "Unit")]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Total quantity available")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="kg")
    stored_date = models.DateField(auto_now_add=True)
    shelf_date = models.DateField(help_text="Expected date of spoilage")
    sold_quantity = models.FloatField(default=0, help_text="Total quantity sold")
    
    @property
    def remaining_stock(self):
        return self.quantity - self.sold_quantity

    def __str__(self):
        return f"{self.crop.name} - {self.quantity} {self.unit} (Remaining: {self.remaining_stock} {self.unit})"

class SpoilageTracking(models.Model):
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE, related_name="spoilage")
    notified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Spoilage Tracking for {self.inventory.crop.name}"
