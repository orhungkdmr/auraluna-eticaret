from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# ProductVariant'ları, Product sayfasının içinde düzenlemek için bir "inline" sınıfı oluşturuyoruz
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1 # Varsayılan olarak 1 tane boş varyasyon satırı gösterir

# ProductImage'ları, Product sayfasının içinde düzenlemek için bir "inline" sınıfı oluşturuyoruz
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Varsayılan olarak 1 tane boş resim yükleme alanı gösterir

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    # "inlines" listesine, ürün detay sayfasında varyasyonları ve ek resimleri
    # aynı anda yönetmemizi sağlayan iki sınıfı da ekliyoruz.
    inlines = [ProductImageInline, ProductVariantInline]

# ProductVariant modelini ayrıca admin'de listeleyerek aranabilir hale getiriyoruz
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'sku', 'price', 'stock')
    list_filter = ('product', 'size', 'color')
    search_fields = ('sku', 'product__name') # SKU ve ürün adına göre arama yapmayı sağlar