from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Inventory, Crop
from .forms import InventoryForm
@login_required
def farmer_stock_view(request):
    inventory_items = Inventory.objects.filter(farmer=request.user)  # Show only logged-in farmer's stock
    return render(request, "users/farmer_stock.html", {"inventory_items": inventory_items})



@login_required
def farmer_stock_view(request):
    inventory_items = Inventory.objects.filter(farmer=request.user)

    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.farmer = request.user  # Assign the logged-in farmer
            stock.save()
            return redirect("farmer_stock")  # Refresh the page after adding stock
    else:
        form = InventoryForm()

    return render(request, "users/farmer_stock.html", {"inventory_items": inventory_items, "form": form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Crop
from .forms import CropForm  # We will create this form

@login_required
def edit_stock(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)

    if request.method == "POST":
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect("farmer_home")  # Redirect to inventory page
    else:
        form = CropForm(instance=crop)

    return render(request, "users/edit_stock.html", {"form": form, "crop": crop})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inventory, Crop
from .forms import InventoryForm

@login_required
def farmer_stock_view(request):
    stock_items = Inventory.objects.filter(farmer=request.user)
    return render(request, "inventory/farmer_stock.html", {"stock_items": stock_items})

@login_required
def add_stock(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.farmer = request.user  # Assign logged-in farmer
            stock.save()
            messages.success(request, "Stock added successfully!")
            return redirect("farmer_stock")
    else:
        form = InventoryForm()
    return render(request, "inventory/stock_form.html", {"form": form})

@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(Inventory, id=stock_id, farmer=request.user)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock updated successfully!")
            return redirect("farmer_stock")
    else:
        form = InventoryForm(instance=stock)
    return render(request, "inventory/stock_form.html", {"form": form})

@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Inventory, id=stock_id, farmer=request.user)
    stock.delete()
    messages.success(request, "Stock deleted successfully!")
    return redirect("farmer_stock")

