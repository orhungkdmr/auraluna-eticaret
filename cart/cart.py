from decimal import Decimal
from django.conf import settings
from products.models import Product, ProductVariant

class Cart:
    def __init__(self, request):
        """
        Sepeti başlatır.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # session'da yeni bir sepet oluştur
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1, override_quantity=False):
        """
        Ürün VARYASYONUNU sepete ekler veya miktarını günceller.
        """
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': str(variant.price)}
        
        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity
        self.save()

    def save(self):
        # session'ı "modified" olarak işaretle, kaydedildiğinden emin ol
        self.session.modified = True

    def remove(self, variant):
        """
        Varyasyonu sepetten siler.
        """
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def __iter__(self):
        """
        Session'daki veriyi okur, veritabanından nesneleri alır ve şablon için
        geçici bir veri yapısı oluşturur. Session'ı ASLA DEĞİŞTİRMEZ.
        """
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids)
        
        variants_dict = {str(v.id): v for v in variants}

        for variant_id, item_data in self.cart.items():
            yield {
                'quantity': item_data['quantity'],
                'price': Decimal(item_data['price']),
                'variant': variants_dict.get(variant_id),
                'total_price': Decimal(item_data['price']) * item_data['quantity']
            }

    def __len__(self):
        """
        Sepetteki toplam ürün adedini (miktarların toplamını) sayar.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Sepetin toplam maliyetini hesaplar.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # sepeti session'dan sil
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()