from django import forms
from .models import Inventory,Crop

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["crop", "quantity", "unit", "shelf_date"]
        widgets = {
            "shelf_date": forms.DateInput(attrs={"type": "date"}),  # Date picker for shelf date
        }


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ["name", "shelf_life_days"]