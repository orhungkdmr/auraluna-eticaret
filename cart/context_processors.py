from .cart import Cart
from products.models import Category

def cart(request):
    """
    Tüm şablonların 'cart' değişkenine erişmesini sağlar.
    Bu, menüdeki sepet sayacını anlık olarak güncellemek için kullanılır.
    """
    return {'cart': Cart(request)}

def main_categories(request):
    """
    Tüm şablonların ana kategorilere ('main_categories') erişmesini sağlar.
    Bu, navigasyon menüsündeki 'Ürünler' sekmesini doldurmak için kullanılır.
    """
    # Sadece parent'ı olmayan, yani ana kategorileri veritabanından çeker.
    return {'main_categories': Category.objects.filter(parent__isnull=True)}