from django.shortcuts import render

# Create your views here.

from .models import Message

def contact(request):
    if 'cuname' in request.POST:
        cuname = request.POST['cuname']
        email = request.POST['email']
        title = request.POST['title']
        content = request.POST['content']
        
        
        obj = Message.objects.create(name=cuname, email=email, subject=title, content=content)
        obj.save()
        
    return render(request, 'contact.html')



