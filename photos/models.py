from django.db import models

# Create your models here.

from django.utils import timezone

#當 django 要使用圖片上傳功能時，要先安裝 pillow
#指令 pip install pillow


class Photos(models.Model):
    #upload_to 圖片上傳後存放的路徑位置
    #blank, null 這兩個是表示圖片欄位是否可以為空值，Fales代表不能為空值
    
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    upload_date = models.DateField(default=timezone.now)
    
    
    
    