from django.shortcuts import render

from .models import Tour

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

# Create your views here.

def tour(request):
    
    p = ''
    sprice = ''
    eprice = ''
    
    allTours = Tour.objects.all().order_by('-id')
    #order_by 排序，id 是欄位名稱 order_by('id') 依 id 做遞增
    #order_by('-id') 依 id 做遞減
    
    paginator = Paginator(allTours, 2) #2筆為一頁
    page = request.GET.get('page')
    try:
        allTours = paginator.page(page)
    except PageNotAnInteger:
        allTours = paginator.page(1) #非整數時就跳到第一頁
    except EmptyPage:
        allTours = paginator.page(paginator.num_pages) #跳至最後一頁
    
    content = {'tours': allTours, "product":p, "startp":sprice, "endp":eprice}
    return render(request, 'travel.html', content)
    # locals() 將函式中的變數整個帶過去給 travel.html


def index(request):
    
    if 'UserEmail' in request.COOKIES:
        uemail = request.COOKIES['UserEmail']
    else:
        uemail = ''                             
                    
    
    
    return render(request, 'index.html', locals())

