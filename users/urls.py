from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("customer_home/", views.customer_home, name="customer_home"),
    path("farmer_home/", views.farmer_home, name="farmer_home"),
    path("admin_home/", views.admin_home, name="admin_home"),
     path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
]

