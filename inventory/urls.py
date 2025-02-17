from django.urls import path
from .views import farmer_stock_view, add_stock, edit_stock, delete_stock

urlpatterns = [
    path("farmer/stock/", farmer_stock_view, name="farmer_stock"),
    path("farmer/stock/add/", add_stock, name="add_stock"),
    path("farmer/stock/edit/<int:stock_id>/", edit_stock, name="edit_stock"),
    path("farmer/stock/delete/<int:stock_id>/", delete_stock, name="delete_stock"),
]
