from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def product_list(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    # Sadece en az bir varyasyonu olan ürünleri listele
    product_list = Product.objects.filter(variants__isnull=False).distinct().order_by('-created_at')

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        # Ana kategori seçildiyse, tüm alt kategorilerindeki ürünleri al
        if not current_category.parent:
            product_list = product_list.filter(category__in=current_category.children.all())
        # Alt kategori seçildiyse, sadece o kategorideki ürünleri al
        else:
            product_list = product_list.filter(category=current_category)

    # Arama mantığı
    query = request.GET.get('q')
    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    paginator = Paginator(product_list, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'current_category': current_category
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants_queryset = product.variants.all()
    # JSON için veriyi Python'da listeye çevir
    variants_list = list(variants_queryset.values('id', 'size', 'color', 'stock', 'price'))
    product_images = product.images.all()
    
    # Benzer ürünler
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'variants': variants_list,
        'product_images': product_images,
        'similar_products': similar_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_quick_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants_list = list(product.variants.all().values('id', 'size', 'color', 'stock', 'price'))
    images_list = [img.image.url for img in product.images.all()]
    main_image_url = product.image.url if product.image else None
    
    data = {
        'name': product.name,
        'description': product.description,
        'category': str(product.category),
        'main_image': main_image_url,
        'gallery_images': images_list,
        'variants': variants_list,
        'add_to_cart_url_base': reverse('cart:cart_add', args=[0]),
    }
    return JsonResponse(data)


@login_required
def toggle_favourite(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    is_favourited = False
    message = ""
    if product.favourited_by.filter(id=request.user.id).exists():
        product.favourited_by.remove(request.user)
        message = f"'{product.name}' favorilerinizden kaldırıldı."
    else:
        product.favourited_by.add(request.user)
        message = f"'{product.name}' favorilerinize eklendi."
        is_favourited = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'message': message,
            'is_favourited': is_favourited
        })
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

@login_required
def favourite_list(request):
    favourite_products = request.user.favourite_products.all()
    context = {'favourite_products': favourite_products}
    return render(request, 'products/favourite_list.html', context)