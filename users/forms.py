from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username","email", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.generate_unique_username(user.email)  # Generate a unique username
        if commit:
            user.save()
        return user

    def generate_unique_username(self, email):
        base_username = email.split("@")[0]  # Use email prefix as base username
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"  # Append a number if username exists
            counter += 1
        return username
