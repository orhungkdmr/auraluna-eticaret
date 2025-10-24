from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import ProductVariant
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse

@require_POST
def cart_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1 # Geçersiz bir değer gelirse varsayılan olarak 1 al
        
    # Stok kontrolü
    if variant.stock < quantity:
        message = f"'{variant}' için yeterli stok bulunmuyor. Sadece {variant.stock} adet eklenebilir."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': message}, status=400)
        messages.error(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

    cart.add(variant=variant, quantity=quantity)
    message = f"{quantity} adet '{variant}' sepete eklendi."
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'message': message, 'cart_total_items': len(cart)})
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

@require_POST
def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    message = f"'{variant}' sepetten kaldırıldı."
    
    # Sepet sayfasındaki silme işlemi AJAX ile yapıldığında, sayfanın yeniden yüklenmesi gerekir.
    # Bu yüzden özel bir durum ve JSON cevabı gönderiyoruz.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'reload', 'message': message, 'cart_total_items': len(cart)})
    
    messages.success(request, message)
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    try:
        quantity = int(request.POST.get('quantity'))
        
        # Stok kontrolü
        if quantity > variant.stock:
            message = f"'{variant}' için stok aşıldı. En fazla {variant.stock} adet eklenebilir."
            messages.error(request, message)
        elif quantity > 0:
            cart.add(variant=variant, quantity=quantity, override_quantity=True)
            messages.success(request, "Sepetiniz güncellendi.")
        else:
            cart.remove(variant)
            messages.success(request, f"'{variant}' sepetten kaldırıldı.")
            
    except (ValueError, TypeError):
        messages.error(request, "Geçersiz miktar.")
    
    # Miktar güncellemesi her zaman sepet sayfasında yapılır, bu yüzden her zaman oraya yönlendiririz.
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})