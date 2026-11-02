from django.shortcuts import render
from categories.models import Category

def home_view(request):
    """Home page view with featured categories"""
    categories = Category.objects.filter(is_active=True)[:6]
    return render(request, 'base/home.html', {'categories': categories})