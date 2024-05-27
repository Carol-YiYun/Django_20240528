from django.contrib import admin

# Register your models here.

from cart import models

admin.site.register(models.OrdersModel)
admin.site.register(models.DetailModel)