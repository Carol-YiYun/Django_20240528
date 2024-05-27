from django.db import models

# Create your models here.

class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    granttotal = models.IntegerField(default=0)
    customname = models.CharField(max_length=100)
    customemail = models.CharField(max_length=100)
    customphone = models.CharField(max_length=50)
    customaddress = models.CharField(max_length=200)
    paytype = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.customname
    
class DetailModel(models.Model):
    #↓這裡的OrdersModel要等於上面的class，就是客戶的訂單編號，所以是外來鍵（會重複）
    dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname
    
    
    
    
    
    
    
    
    