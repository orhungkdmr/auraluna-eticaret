from django.contrib import admin
from .models import Slide

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    """
    'Slide' modelinin admin panelinde nasıl görüneceğini ve yönetileceğini belirler.
    """
    # Slaytları listelerken başlığını ve sırasını göster
    list_display = ('title', 'order')
    # Liste ekranından doğrudan 'order' alanını düzenlemeye izin ver
    list_editable = ('order',)