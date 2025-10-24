from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        full_path = [self.name]; k = self.parent
        while k is not None: full_path.append(k.name); k = k.parent
        return ' > '.join(full_path[::-1])
    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Ana kapak fotoğrafı")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favourited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourite_products', blank=True)
    class Meta:
        ordering = ('-created_at',)
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('products:product_detail', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True, help_text="Resim yüklenemezse görünecek alternatif metin.")
    def __str__(self): return f"{self.product.name} - Resim {self.id}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    
    # YENİ SKU ALANI
    sku = models.CharField(max_length=100, unique=True, help_text="Benzersiz Stok Kodu (SKU), örn: AUR-GM-BYZ-M")
    
    size = models.CharField(max_length=10, help_text='Örn: S, M, L, XL')
    color = models.CharField(max_length=50, help_text='Örn: Beyaz, Mavi, Siyah')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('product', 'size', 'color')
    def __str__(self): return f'{self.product.name} - {self.size} / {self.color}'