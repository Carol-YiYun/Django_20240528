from django.shortcuts import render

from .models import Goods, GoodsItems

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def product(request):
    
    p = ''
    sprice = ''
    eprice = ''
    itemtype = 0
    
    #網址中是否有參數名稱為 goods，代表是否有按"查詢"按鈕
    if "goods" in request.GET:
        
        p = request.GET['goods']
        sprice = request.GET['startprice']
        eprice = request.GET['endprice']
        itemtype = request.GET['items']
        
        if len(itemtype) == 0:
            itemtype = 0
        
        
        #代表使用者只輸入商品名稱，使用關鍵字查詢，並沒有輸入價格和種類
        if ( len(p) > 0 and len(sprice) == 0 and len(eprice) == 0 and itemtype == "0"):
            
            allGoods = Goods.objects.filter(title__contains=p).order_by('price')
        
        #代表使用者有輸入商品名稱，使用關鍵字查詢，並且有輸入種類
        elif ( len(p) > 0 and len(sprice) == 0 and len(eprice) == 0 and itemtype != "0"):
            
            allGoods = Goods.objects.filter(title__contains=p, items=itemtype).order_by('price')
        
        #代表使用者有輸入商品名稱，使用關鍵字查詢，並且有輸入價格，但沒輸入種類
        elif ( len(p) > 0 and len(sprice) > 0 and len(eprice) > 0 and itemtype == "0"):
            
            allGoods = Goods.objects.filter(title__contains=p, price__gte=sprice, price__lte = eprice).order_by('price')
        
        #代表使用者全部欄位都有輸入
        elif ( len(p) > 0 and len(sprice) > 0 and len(eprice) > 0 and itemtype != "0"):
            
            allGoods = Goods.objects.filter(title__contains=p, price__gte=sprice, price__lte = eprice, items=itemtype).order_by('price')
            
        #代表使用者只輸入價格
        elif ( len(p) == 0 and len(sprice) > 0 and len(eprice) > 0 and itemtype == "0"):
            
            allGoods = Goods.objects.filter(price__gte=sprice, price__lte = eprice).order_by('price')
            
        #代表使用者有輸入價格和種類
        elif ( len(p) == 0 and len(sprice) > 0 and len(eprice) > 0 and itemtype != "0"):
            
            allGoods = Goods.objects.filter(price__gte=sprice, price__lte = eprice, items=itemtype).order_by('price')
        
        #代表使用者只選種類
        elif ( len(p) == 0 and len(sprice) == 0 and len(eprice) == 0 and itemtype != "0"):
            
            allGoods = Goods.objects.filter(items=itemtype).order_by('price')
        
            
        else:
            allGoods = Goods.objects.all().order_by('-id')
        
    else:
        allGoods = Goods.objects.all().order_by('-id')
    
    
    
    paginator = Paginator(allGoods, 2) #2筆為一頁
    page = request.GET.get('page')
    try:
        allGoods = paginator.page(page)
    except PageNotAnInteger:
        allGoods = paginator.page(1) #非整數時就跳到第一頁
    except EmptyPage:
        allGoods = paginator.page(paginator.num_pages) #跳至最後一頁
    
    
    
    content = {'goods': allGoods, "product":p, "startp":sprice, "endp":eprice, "items":itemtype}
    return render(request, 'product.html', content)



