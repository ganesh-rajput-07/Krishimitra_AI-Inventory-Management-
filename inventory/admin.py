from django.contrib import admin
from .models import Crop, Inventory, SpoilageTracking

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "shelf_life_days")
    search_fields = ("name",)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("farmer", "crop", "quantity", "stored_date", "shelf_date")
    list_filter = ("crop", "shelf_date")
    search_fields = ("crop__name", "farmer__username")

@admin.register(SpoilageTracking)
class SpoilageTrackingAdmin(admin.ModelAdmin):
    list_display = ("inventory", "notified")
    list_filter = ("notified",)
