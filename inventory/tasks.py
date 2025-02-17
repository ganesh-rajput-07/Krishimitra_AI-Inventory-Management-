from celery import shared_task
from django.utils.timezone import now
from .models import Inventory

@shared_task
def check_spoilage():
    today = now().date()
    expired_items = Inventory.objects.filter(shelf_date__lte=today)
    
    for item in expired_items:
        # Send notification (can be email, SMS, or app notification)
        print(f"⚠️ Spoilage Alert: {item.crop.name} expired on {item.shelf_date}")

    return f"{expired_items.count()} items expired."
