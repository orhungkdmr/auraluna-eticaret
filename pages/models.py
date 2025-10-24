from django.db import models

class Slide(models.Model):
    """
    Ana sayfadaki tam sayfa karuselde görünecek her bir slaytı temsil eder.
    """
    image = models.ImageField(upload_to='slides/')
    title = models.CharField(max_length=200, help_text="Slaytın ana başlığı (büyük yazılacak)")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Başlığın altındaki daha küçük metin (isteğe bağlı)")
    button_text = models.CharField(max_length=50, default="Keşfet", help_text="Slayt üzerindeki butonun metni")
    button_link = models.CharField(max_length=200, default="/products/", help_text="Butona tıklandığında gidilecek adres (örn: /products/erkek/)")
    order = models.PositiveIntegerField(default=0, help_text="Gösterim sırası (küçük olan önce gelir)")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title