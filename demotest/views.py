from django.shortcuts import render

# Create your views here.

def test(request):
    
    name = 'John'
    age = 20
    
    score = 70
    
    listdata = range(1,10)
    
    
    
    
    
    return render(request, 'BasePage.html', locals())



