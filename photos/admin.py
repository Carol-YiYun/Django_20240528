from django.contrib import admin

# Register your models here.


from .models import Photos

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'upload_date')
    
    

admin.site.register(Photos, PhotoAdmin)