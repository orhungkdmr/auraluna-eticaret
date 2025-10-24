from django.urls import path
from .views import home_view, about_view, contact_view

app_name = 'pages'

urlpatterns = [
    # Ana sayfa (örn: /)
    path('', home_view, name='home'),
    
    # Hakkımızda sayfası (örn: /about/)
    path('about/', about_view, name='about'),
    
    # İletişim sayfası (örn: /contact/)
    path('contact/', contact_view, name='contact'),
]