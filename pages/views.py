from django.shortcuts import render
from products.models import Product
from .models import Slide

def home_view(request):
    """
    Ana sayfayı oluşturur. Veritabanından en yeni ürünleri ve
    ana sayfa karuseli için slaytları çeker.
    """
    # Sadece en az bir varyasyonu olan, en yeni 8 ürünü al
    new_products = Product.objects.filter(variants__isnull=False).distinct().order_by('-created_at')[:8]
    
    # Tüm slaytları al
    slides = Slide.objects.all()
    
    context = {
        'new_products': new_products,
        'slides': slides,
    }
    return render(request, 'pages/home.html', context)

def about_view(request):
    """
    Hakkımızda sayfasını gösterir.
    """
    return render(request, 'pages/about.html')

def contact_view(request):
    """
    İletişim sayfasını gösterir.
    """
    return render(request, 'pages/contact.html')