from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin paneli URL'i
    path('admin/', admin.site.urls),

    # Uygulamalarımızın URL'lerini dahil ediyoruz
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),

    # Django'nun hazır üyelik sistemi URL'leri (giriş, çıkış, şifre sıfırlama vb.)
    path('accounts/', include('django.contrib.auth.urls')),
    # Bizim kendi 'signup' (kayıt ol) URL'imiz
    path('accounts/', include('accounts.urls')),

    # Statik sayfalar (ana sayfa, hakkımızda vb.)
    # Bu boş path ('') sayesinde ana sayfa olur.
    path('', include('pages.urls')),
    
    # Ürünler uygulaması URL'leri
    path('products/', include('products.urls')),
]

# Geliştirme ortamında, kullanıcıların yüklediği resimleri (media dosyaları) gösterebilmek için
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)