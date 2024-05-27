"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from travel.views import tour,index

from demotest.views import test

from product.views import product

from cart.views import cart, addtocart, cartorder, cartok, cartordercheck, ECPayCredit, myorder

from contact.views import contact

from member.views import register, login, logout, forget, changepassword, member

from photos.views import index as photoindex

from django.conf import settings
from django.conf.urls.static import static

from sendmail.views import sendmail



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path('travel/', tour),
    path('test/', test),
    path('product/', product),
    path('cart/', cart),
    path('addtocart/<str:ctype>/', addtocart),
    path('addtocart/<str:ctype>/<int:productid>/', addtocart),
    path('cartorder/', cartorder),
    path('cartok/', cartok),
    path('cartordercheck/', cartordercheck),
    path('contact/', contact),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('forget/', forget),
    path('changepassword/', changepassword),
    path('photos/', photoindex),
    path('sendmail/', sendmail),
    path('creditcard/', ECPayCredit),
    path('member/', member),
    path('orderlist/', myorder),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
    
    
    
    
    
    
    
    
    