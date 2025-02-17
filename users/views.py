import logging
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomUserCreationForm
from .models import CustomUser
from inventory.models import Inventory
import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Landing Page (Pre-Login)
def landing(request):
    if request.user.is_authenticated:
        return redirect(reverse(f"{request.user.user_type}_home"))
    return render(request, "landing.html")

# User Login
def user_login(request):
    logger.debug("Entered user_login view")

    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user_obj = CustomUser.objects.get(email__iexact=identifier)
            username = user_obj.username
        except CustomUser.DoesNotExist:
            username = identifier

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                messages.error(request, "Please verify your email before logging in.")
                return redirect("login")

            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(reverse(f"{user.user_type}_home"))
        
        messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, "users/login.html")

# User Logout
def user_logout(request):
    logout(request)
    return redirect(reverse("login"))
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        user_type = request.POST.get("user_type", "customer")  # Default to customer

        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = user_type
            user.is_active = False  # Email verification required
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse("activate_account", kwargs={"uidb64": uid, "token": token})
            )

            subject = "Verify Your Email - KrishiMitra AI"
            html_message = render_to_string("users/activation_email.html", {"activation_link": activation_link})
            send_mail(subject, "", "your-email@gmail.com", [user.email], html_message=html_message)

            messages.success(request, "Account created! Check your email to verify your account.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})

# Email Activation
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verified! You can now log in.")
            return redirect("login")
        
        messages.error(request, "Invalid activation link.")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, "Invalid activation link.")
    
    return redirect("register")

# Home Pages
@login_required
def customer_home(request):
    return render(request, "users/customer_home.html")

@login_required
def farmer_home(request):
    return render(request, "users/farmer_home.html")

@login_required
def admin_home(request):
    return render(request, "users/admin_home.html")

@login_required
def farmer_dashboard(request):
    today = datetime.date.today()
    upcoming_spoilage = Inventory.objects.filter(farmer=request.user, shelf_date__lte=today)

    return render(request, "users/farmer_home.html", {"spoilage_items": upcoming_spoilage})