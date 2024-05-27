from django.db import models

# Create your models here.

class Tour(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField()
    photo_url = models.CharField(max_length=254)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'travel'
        
    
    
    