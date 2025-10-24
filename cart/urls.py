from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Sepet detay sayfası (örn: /cart/)
    path('', views.cart_detail, name='cart_detail'),
    
    # Sepete ekleme işlemi (örn: /cart/add/5/)
    path('add/<int:variant_id>/', views.cart_add, name='cart_add'),
    
    # Sepetten silme işlemi (örn: /cart/remove/5/)
    path('remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
    
    # Sepet miktarını güncelleme işlemi (örn: /cart/update/5/)
    path('update/<int:variant_id>/', views.cart_update, name='cart_update'),
]