from django.shortcuts import render
import hashlib
from .models import Member

from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

def register(request):
    if 'cuname' in request.POST:
        
        username = request.POST['cuname']
        email = request.POST['email']
        password = request.POST['pwd']
        sex = request.POST['sex']
        tel = request.POST['phone']
        birthday = request.POST['birthday']
        address = request.POST['address']
        
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        obj = Member.objects.filter(email=email).count() #檢查此email是否已存在於資料庫中
        if obj == 0: #代表此email不存在於資料庫中
            #新增資料進資料庫
            Member.objects.create(name=username, sex=sex, birthday=birthday, email=email, phone=tel, address=address, password=password)
            msg = "註冊成功！"
        else:
            msg = "此Email帳號已經存在，請使用其他Email註冊。"
            
    return render(request, 'register.html', locals())


def login(request):
    
    msg = ""
    if "email" in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        #確認帳密是否存在於資料庫
        obj = Member.objects.filter(email=email, password=password).count() #計算符合的筆數
        if obj > 0: #表示此使用者存在於資料庫，且帳密都對
            request.session["myMail"] = email #儲存session資料，一般來說能存14天
            request.session["isAlive"] = True
            
            #加 Cookies 功能，若使用者禁用時，就會無效。
            
            #宣告 Cookies 物件
            
            response = HttpResponseRedirect('/') # 指向根目錄
            
            
            # max_age 是指該 Cookies 能存活 1200 秒 = 20分鐘
            response.set_cookie('UserEmail', email, max_age=1200)
            
            return response # 切換到 index.html
        else:
            msg = "帳密錯誤，請重新輸入。"
            return render(request, 'login.html', locals())
        
    else:
        return render(request, 'login.html', locals())
        


def logout(request):
    del request.session["isAlive"]
    del request.session["myMail"]
    return HttpResponseRedirect('/login')


def forget(request):
    pass

def changepassword(request):
    msg = ''
    if "password" in request.POST:
        
        oldpwd = request.POST['password']
        repwd = request.POST['repassword']
        
        if oldpwd == repwd:
            changedpwd = hashlib.sha3_256(oldpwd.encode('utf-8')).hexdigest()
            email = request.session['myMail']
            
            user = Member.objects.get(email=email)
            user.password = changedpwd
            user.save()
            msg = "密碼變更完成！"
        else:
            msg = "兩次輸入的密碼不相同"
            
    return render(request, 'member.html', locals())


def member(request):
    
    # 確認使用者是否已登入
    if "myMail" in request.session and "isAlive" in request.session: 
        return render(request, 'member.html')
    else:
        return HttpResponseRedirect('/login')











