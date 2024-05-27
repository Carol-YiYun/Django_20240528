from django.db import models

# Create your models here.

class Goods(models.Model):
    platform = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    photo_url  = models.CharField(max_length=255)
    goods_url  = models.CharField(max_length=255)
    items = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'goods'
        

class GoodsItems(models.Model):
    itemName = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'items'
        
        
    
    