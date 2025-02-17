import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from inventory.models import Inventory, SpoilageTracking

class Command(BaseCommand):
    help = "Checks inventory for spoilage and notifies farmers"

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        spoilage_items = Inventory.objects.filter(shelf_date__lte=today)

        for item in spoilage_items:
            tracking, created = SpoilageTracking.objects.get_or_create(inventory=item)

            if not tracking.notified:  # If notification hasn't been sent yet
                farmer_email = item.farmer.email
                subject = f"⚠️ Spoilage Alert: {item.crop.name}"
                message = f"Dear {item.farmer.username},\n\nYour crop '{item.crop.name}' stored on {item.stored_date} is expected to spoil today ({item.shelf_date}). Please take necessary action.\n\nRegards,\nKrishiMitra AI"

                send_mail(subject, message, "your-email@gmail.com", [farmer_email])

                tracking.notified = True
                tracking.save()
                self.stdout.write(self.style.SUCCESS(f"Notification sent to {farmer_email}"))

        self.stdout.write(self.style.SUCCESS("Spoilage check completed."))
