from django.contrib import admin

# Register your models here.

#客製化後台顯示欄位

from .models import Goods, GoodsItems

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('platform', 'title', 'price')
    
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'itemName')
    
    
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsItems, ItemsAdmin)

    
    
    